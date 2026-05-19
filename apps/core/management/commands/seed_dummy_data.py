from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from rest_framework.authtoken.models import Token

from apps.chats.models import ChatRoom, Message
from apps.chats.services import cleanup_expired_chatrooms, create_chatroom, send_message
from apps.reports.models import Report
from apps.reports.models import ReportStatus
from apps.reports.services import create_report
from apps.users.models import User


class Command(BaseCommand):
    help = "Seed data dummy untuk development (users, reports, chats, messages)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Hapus data existing (kecuali superuser) sebelum seed.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if options["reset"]:
            self._reset_data()

        users = self._seed_users()
        reports = self._seed_reports(users)
        self._seed_chats(users, reports)

        active_chat_count = ChatRoom.objects.count()
        message_count = Message.objects.count()
        report_count = Report.objects.count()
        user_count = User.objects.filter(is_superuser=False).count()

        self.stdout.write(
            self.style.SUCCESS(
                "Seed selesai: "
                f"{user_count} user biasa, {report_count} laporan, "
                f"{active_chat_count} chat room, {message_count} pesan."
            )
        )

    def _reset_data(self):
        Message.objects.all().delete()
        ChatRoom.objects.all().delete()
        Report.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()
        self.stdout.write(self.style.WARNING("Data lama (non-superuser) sudah dihapus."))

    def _seed_users(self):
        user_payloads = [
            {
                "email": "andi@umkt.ac.id",
                "name": "Andi Pratama",
                "password": "AndiPass123!",
            },
            {
                "email": "bunga@umkt.ac.id",
                "name": "Bunga Lestari",
                "password": "BungaPass123!",
            },
            {
                "email": "citra@umkt.ac.id",
                "name": "Citra Nuraini",
                "password": "CitraPass123!",
            },
            {
                "email": "doni@umkt.ac.id",
                "name": "Doni Saputra",
                "password": "DoniPass123!",
            },
            {
                "email": "eka@umkt.ac.id",
                "name": "Eka Maulana",
                "password": "EkaPass123!",
            },
        ]
        users = {}
        for payload in user_payloads:
            user, created = User.objects.get_or_create(
                email=payload["email"],
                defaults={"name": payload["name"]},
            )
            if created:
                user.set_password(payload["password"])
                user.save(update_fields=["password"])
            else:
                user.name = payload["name"]
                user.save(update_fields=["name"])

            Token.objects.get_or_create(user=user)
            users[payload["email"]] = user
            self.stdout.write(
                f"- User {payload['email']} ({'created' if created else 'exists'})"
            )
        return users

    def _seed_reports(self, users):
        report_payloads = [
            {
                "owner": "andi@umkt.ac.id",
                "title": "Dompet hitam hilang di Perpustakaan",
                "description": "Berisi KTM dan kartu ATM, terakhir terlihat di lantai 2 perpustakaan.",
                "location": "Perpustakaan Lantai 2",
                "status": ReportStatus.LOST,
            },
            {
                "owner": "bunga@umkt.ac.id",
                "title": "Ditemukan kunci motor di parkiran FIK",
                "description": "Kunci motor dengan gantungan merah ditemukan dekat pos satpam.",
                "location": "Parkiran FIK",
                "status": ReportStatus.FOUND,
            },
            {
                "owner": "citra@umkt.ac.id",
                "title": "Laptop silver sudah diklaim pemilik",
                "description": "Laptop ditemukan di kantin, sekarang sudah kembali ke pemilik.",
                "location": "Kantin Utama",
                "status": ReportStatus.CLAIMED,
            },
            {
                "owner": "doni@umkt.ac.id",
                "title": "ID Card mahasiswa hilang",
                "description": "ID Card atas nama Doni kemungkinan jatuh di sekitar auditorium.",
                "location": "Auditorium",
                "status": ReportStatus.LOST,
            },
            {
                "owner": "eka@umkt.ac.id",
                "title": "Ditemukan tumbler biru di mushola",
                "description": "Tumbler biru polos tanpa nama ditemukan setelah dzuhur.",
                "location": "Mushola Kampus",
                "status": ReportStatus.FOUND,
            },
        ]

        reports = {}
        for payload in report_payloads:
            owner = users[payload["owner"]]
            report = Report.objects.filter(user=owner, title=payload["title"]).first()
            if not report:
                report = create_report(
                    user=owner,
                    title=payload["title"],
                    description=payload["description"],
                    location=payload["location"],
                    status=payload["status"],
                )
                created = True
            else:
                report.description = payload["description"]
                report.location = payload["location"]
                report.status = payload["status"]
                report.save(update_fields=["description", "location", "status"])
                created = False

            reports[payload["title"]] = report
            self.stdout.write(
                f"- Report '{payload['title']}' ({'created' if created else 'exists'})"
            )

        return reports

    def _seed_chats(self, users, reports):
        active_report = reports["Dompet hitam hilang di Perpustakaan"]
        active_chat, _ = create_chatroom(report=active_report, initiator=users["bunga@umkt.ac.id"])
        if not active_chat.messages.exists():
            send_message(
                chatroom=active_chat,
                sender=users["bunga@umkt.ac.id"],
                message="Halo kak, saya lihat dompet hitam di dekat rak referensi.",
            )
            send_message(
                chatroom=active_chat,
                sender=users["andi@umkt.ac.id"],
                message="Terima kasih infonya, saya cek sekarang.",
            )

        readonly_report = reports["ID Card mahasiswa hilang"]
        readonly_chat, _ = create_chatroom(
            report=readonly_report,
            initiator=users["eka@umkt.ac.id"],
        )
        if not readonly_chat.messages.exists():
            send_message(
                chatroom=readonly_chat,
                sender=users["eka@umkt.ac.id"],
                message="Saya sempat lihat kartu mirip ID Card di dekat auditorium.",
            )
            send_message(
                chatroom=readonly_chat,
                sender=users["doni@umkt.ac.id"],
                message="Baik, nanti saya cek. Terima kasih.",
            )

        readonly_time = timezone.now() - timedelta(days=3)
        ChatRoom.objects.filter(id=readonly_chat.id).update(created_at=readonly_time)
        Message.objects.filter(chatroom=readonly_chat).update(created_at=readonly_time)

        expired_report = reports["Ditemukan tumbler biru di mushola"]
        expired_chat, _ = create_chatroom(
            report=expired_report,
            initiator=users["andi@umkt.ac.id"],
        )
        if not expired_chat.messages.exists():
            send_message(
                chatroom=expired_chat,
                sender=users["andi@umkt.ac.id"],
                message="Apakah tumbler masih ada? Saya merasa itu milik teman saya.",
            )
        expired_time = timezone.now() - timedelta(days=8)
        ChatRoom.objects.filter(id=expired_chat.id).update(created_at=expired_time)
        Message.objects.filter(chatroom=expired_chat).update(created_at=expired_time)

        purged = cleanup_expired_chatrooms()
        self.stdout.write(f"- Chat expired yang dibersihkan: {purged}")
