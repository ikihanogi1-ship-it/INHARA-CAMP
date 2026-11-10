import unittest
from datetime import date, timedelta
from pathlib import Path
from tempfile import TemporaryDirectory

import app
from app import available_stock, calculate_fine, rental_days


class RentalCalculationTests(unittest.TestCase):
    def test_same_day_rental_is_charged_for_one_day(self):
        self.assertEqual(rental_days(date(2026, 11, 10), date(2026, 11, 10)), 1)

    def test_duration_matches_planned_return_date_difference(self):
        self.assertEqual(rental_days(date(2026, 11, 10), date(2026, 11, 13)), 3)

    def test_late_fee_is_twenty_percent_per_unit_per_late_day(self):
        self.assertEqual(calculate_fine(2, 2, 100000), 80000)

    def test_availability_accounts_for_overlapping_rentals(self):
        bookings = [
            (date(2026, 11, 10), date(2026, 11, 13), None, 2),
            (date(2026, 11, 12), date(2026, 11, 15), None, 1),
        ]
        self.assertEqual(
            available_stock(
                4, date(2026, 11, 11), date(2026, 11, 14), bookings
            ),
            1,
        )

    def test_returned_equipment_is_available_after_actual_return(self):
        bookings = [
            (
                date(2026, 11, 10),
                date(2026, 11, 15),
                date(2026, 11, 12),
                2,
            )
        ]
        self.assertEqual(
            available_stock(
                2, date(2026, 11, 12), date(2026, 11, 14), bookings
            ),
            0,
        )
        self.assertEqual(
            available_stock(
                2, date(2026, 11, 13), date(2026, 11, 14), bookings
            ),
            2,
        )


class RentalDatabaseTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = TemporaryDirectory()
        self.original_db_path = app.DB_PATH
        app.DB_PATH = Path(self.temp_dir.name) / "test.db"
        app.init_db()
        with app.connect_db() as connection:
            self.equipment_id = connection.execute(
                "SELECT id FROM equipment WHERE equipment_name = 'Tenda 4 Orang'"
            ).fetchone()["id"]

    def tearDown(self):
        app.DB_PATH = self.original_db_path
        self.temp_dir.cleanup()

    def make_rental(self, start, due, quantity=1, phone="08123456789"):
        return app.save_rental(
            "Penyewa Uji",
            "Alamat Uji",
            phone,
            start,
            due,
            {self.equipment_id: quantity},
        )

    def test_saving_rental_snapshots_current_rate_and_rejects_overbooking(self):
        first_code = self.make_rental(
            date(2026, 11, 10), date(2026, 11, 13), quantity=3
        )
        self.assertEqual(first_code, "TRX000001")
        with app.connect_db() as connection:
            first = connection.execute(
                """
                SELECT t.total, d.daily_rate
                FROM rental_transactions t
                JOIN rental_details d ON d.transaction_id = t.id
                WHERE t.code = ?
                """,
                (first_code,),
            ).fetchone()
            connection.execute(
                "UPDATE equipment SET daily_rate = 60000 WHERE id = ?",
                (self.equipment_id,),
            )
        self.assertEqual(first["total"], 450000)
        self.assertEqual(first["daily_rate"], 50000)

        with self.assertRaisesRegex(ValueError, "Stok"):
            self.make_rental(
                date(2026, 11, 12),
                date(2026, 11, 14),
                quantity=2,
                phone="08111111111",
            )

    def test_return_records_late_fee(self):
        today = date.today()
        code = self.make_rental(
            today - timedelta(days=5), today - timedelta(days=2)
        )
        with app.connect_db() as connection:
            transaction = connection.execute(
                "SELECT * FROM rental_transactions WHERE code = ?", (code,)
            ).fetchone()

        fine = app.return_transaction(transaction, today)
        self.assertEqual(fine, 20000)
        with app.connect_db() as connection:
            saved = connection.execute(
                "SELECT status, returned_at, fine FROM rental_transactions WHERE code = ?",
                (code,),
            ).fetchone()
        self.assertEqual(saved["status"], "Selesai")
        self.assertEqual(saved["returned_at"], today.isoformat())
        self.assertEqual(saved["fine"], 20000)


if __name__ == "__main__":
    unittest.main()
