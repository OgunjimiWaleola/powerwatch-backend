from django.db import IntegrityError, transaction

from outages.models import Outage
from reports.models import Report


@transaction.atomic
def process_report(report):
    """
    Automatically connect a report to an outage.

    Power Off:
    - Reuse an ongoing outage in the same community.
    - Create one if no ongoing outage exists.
    - Handle simultaneous attempts to create an outage.

    Power Back:
    - Find the ongoing outage.
    - Link the report and mark the outage as restored.
    """

    ongoing_outage = (
        Outage.objects
        .select_for_update()
        .filter(
            community=report.community,
            status=Outage.Status.ONGOING
        )
        .order_by('-started_at')
        .first()
    )

    if report.status == Report.Status.POWER_OFF:

        if ongoing_outage is None:
            try:
                with transaction.atomic():
                    ongoing_outage = Outage.objects.create(
                        community=report.community,
                        started_at=report.reported_at,
                        status=Outage.Status.ONGOING
                    )

            except IntegrityError:
                ongoing_outage = (
                    Outage.objects
                    .select_for_update()
                    .filter(
                        community=report.community,
                        status=Outage.Status.ONGOING
                    )
                    .order_by('-started_at')
                    .first()
                )

                if ongoing_outage is None:
                    raise

        report.outage = ongoing_outage
        report.save(update_fields=['outage'])

    elif report.status == Report.Status.POWER_BACK:

        if ongoing_outage is not None:
            report.outage = ongoing_outage
            report.save(update_fields=['outage'])

            ongoing_outage.status = Outage.Status.RESTORED
            ongoing_outage.restored_at = report.reported_at

            ongoing_outage.save(
                update_fields=[
                    'status',
                    'restored_at',
                    'updated_at'
                ]
            )
