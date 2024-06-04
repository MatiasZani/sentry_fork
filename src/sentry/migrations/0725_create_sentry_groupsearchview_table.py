# Generated by Django 5.0.6 on 2024-05-30 18:53

import django.db.models.constraints
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models

import sentry.db.models.fields.bounded
import sentry.db.models.fields.foreignkey
import sentry.db.models.fields.hybrid_cloud_foreign_key
from sentry.new_migrations.migrations import CheckedMigration


class Migration(CheckedMigration):
    # This flag is used to mark that a migration shouldn't be automatically run in production.
    # This should only be used for operations where it's safe to run the migration after your
    # code has deployed. So this should not be used for most operations that alter the schema
    # of a table.
    # Here are some things that make sense to mark as post deployment:
    # - Large data migrations. Typically we want these to be run manually so that they can be
    #   monitored and not block the deploy for a long period of time while they run.
    # - Adding indexes to large tables. Since this can take a long time, we'd generally prefer to
    #   run this outside deployments so that we don't block them. Note that while adding an index
    #   is a schema change, it's completely safe to run the operation after the code has deployed.
    # Once deployed, run these manually via: https://develop.sentry.dev/database-migrations/#migration-deployment

    is_post_deployment = False

    dependencies = [
        ("sentry", "0724_discover_saved_query_dataset"),
    ]

    operations = [
        migrations.CreateModel(
            name="GroupSearchView",
            fields=[
                (
                    "id",
                    sentry.db.models.fields.bounded.BoundedBigAutoField(
                        primary_key=True, serialize=False
                    ),
                ),
                ("date_updated", models.DateTimeField(default=django.utils.timezone.now)),
                ("date_added", models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ("name", models.TextField(max_length=128)),
                (
                    "user_id",
                    sentry.db.models.fields.hybrid_cloud_foreign_key.HybridCloudForeignKey(
                        "sentry.User", db_index=True, on_delete="CASCADE"
                    ),
                ),
                ("query", models.TextField()),
                ("query_sort", models.CharField(default="date", max_length=16)),
                ("position", models.PositiveSmallIntegerField()),
                (
                    "organization",
                    sentry.db.models.fields.foreignkey.FlexibleForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="sentry.organization"
                    ),
                ),
            ],
            options={
                "db_table": "sentry_groupsearchview",
            },
        ),
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunSQL(
                    sql="""
                        CREATE UNIQUE INDEX CONCURRENTLY "sentry_issueviews_unique_view_position_per_org_user" ON "sentry_groupsearchview" ("user_id", "organization_id", "position");
                    """,
                    hints={"tables": ["sentry_groupsearchview"]},
                ),
                migrations.RunSQL(
                    sql="""
                        ALTER TABLE "sentry_groupsearchview" ADD CONSTRAINT "sentry_issueviews_unique_view_position_per_org_user" UNIQUE USING INDEX "sentry_issueviews_unique_view_position_per_org_user" DEFERRABLE INITIALLY DEFERRED;
                    """,
                    hints={"tables": ["sentry_groupsearchview"]},
                ),
            ],
            state_operations=[
                migrations.AddConstraint(
                    model_name="groupsearchview",
                    constraint=models.UniqueConstraint(
                        deferrable=django.db.models.constraints.Deferrable["DEFERRED"],
                        fields=("user_id", "organization_id", "position"),
                        name="sentry_issueviews_unique_view_position_per_org_user",
                    ),
                ),
            ],
        ),
    ]