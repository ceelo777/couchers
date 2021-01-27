"""Regenerate community migrations

Revision ID: 2affc63b4a01
Revises: 8b6297128973
Create Date: 2021-01-22 19:06:15.660552

"""
import geoalchemy2
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "2affc63b4a01"
down_revision = "8b6297128973"
branch_labels = None
depends_on = None


def upgrade():
    op.execute("CREATE SEQUENCE communities_seq")
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "nodes",
        sa.Column("id", sa.BigInteger(), sa.Sequence("communities_seq"), nullable=False),
        sa.Column("parent_node_id", sa.BigInteger(), nullable=True),
        sa.Column(
            "geom",
            geoalchemy2.types.Geometry(
                geometry_type="MULTIPOLYGON", srid=4326, from_text="ST_GeomFromEWKT", name="geometry"
            ),
            nullable=False,
        ),
        sa.Column("created", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["parent_node_id"], ["nodes.id"], name=op.f("fk_nodes_parent_node_id_nodes")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_nodes")),
    )
    op.create_index(op.f("ix_nodes_parent_node_id"), "nodes", ["parent_node_id"], unique=False)
    op.create_table(
        "threads",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("created", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("deleted", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_threads")),
    )
    op.create_table(
        "clusters",
        sa.Column("id", sa.BigInteger(), sa.Sequence("communities_seq"), nullable=False),
        sa.Column("parent_node_id", sa.BigInteger(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column("created", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("official_cluster_for_node_id", sa.BigInteger(), nullable=True),
        sa.ForeignKeyConstraint(
            ["official_cluster_for_node_id"], ["nodes.id"], name=op.f("fk_clusters_official_cluster_for_node_id_nodes")
        ),
        sa.ForeignKeyConstraint(["parent_node_id"], ["nodes.id"], name=op.f("fk_clusters_parent_node_id_nodes")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_clusters")),
    )
    op.create_index(
        op.f("ix_clusters_official_cluster_for_node_id"), "clusters", ["official_cluster_for_node_id"], unique=True
    )
    op.create_index(op.f("ix_clusters_parent_node_id"), "clusters", ["parent_node_id"], unique=False)
    op.create_table(
        "comments",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("thread_id", sa.BigInteger(), nullable=False),
        sa.Column("author_user_id", sa.BigInteger(), nullable=False),
        sa.Column("content", sa.String(), nullable=False),
        sa.Column("created", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("deleted", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["author_user_id"], ["users.id"], name=op.f("fk_comments_author_user_id_users")),
        sa.ForeignKeyConstraint(["thread_id"], ["threads.id"], name=op.f("fk_comments_thread_id_threads")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_comments")),
    )
    op.create_index(op.f("ix_comments_thread_id"), "comments", ["thread_id"], unique=False)
    op.create_table(
        "discussions",
        sa.Column("id", sa.BigInteger(), sa.Sequence("communities_seq"), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("is_private", sa.Boolean(), nullable=False),
        sa.Column("thread_id", sa.BigInteger(), nullable=False),
        sa.Column("created", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["thread_id"], ["threads.id"], name=op.f("fk_discussions_thread_id_threads")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_discussions")),
    )
    op.create_index(op.f("ix_discussions_thread_id"), "discussions", ["thread_id"], unique=True)
    op.create_table(
        "cluster_discussion_associations",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("discussion_id", sa.BigInteger(), nullable=False),
        sa.Column("cluster_id", sa.BigInteger(), nullable=False),
        sa.ForeignKeyConstraint(
            ["cluster_id"], ["clusters.id"], name=op.f("fk_cluster_discussion_associations_cluster_id_clusters")
        ),
        sa.ForeignKeyConstraint(
            ["discussion_id"],
            ["discussions.id"],
            name=op.f("fk_cluster_discussion_associations_discussion_id_discussions"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_cluster_discussion_associations")),
        sa.UniqueConstraint(
            "discussion_id", "cluster_id", name=op.f("uq_cluster_discussion_associations_discussion_id")
        ),
    )
    op.create_index(
        op.f("ix_cluster_discussion_associations_cluster_id"),
        "cluster_discussion_associations",
        ["cluster_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_cluster_discussion_associations_discussion_id"),
        "cluster_discussion_associations",
        ["discussion_id"],
        unique=False,
    )
    op.create_table(
        "cluster_subscriptions",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("cluster_id", sa.BigInteger(), nullable=False),
        sa.Column("role", sa.Enum("member", "admin", name="clusterrole"), nullable=False),
        sa.Column("joined", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("left", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["cluster_id"], ["clusters.id"], name=op.f("fk_cluster_subscriptions_cluster_id_clusters")
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name=op.f("fk_cluster_subscriptions_user_id_users")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_cluster_subscriptions")),
        sa.UniqueConstraint("user_id", "cluster_id", name=op.f("uq_cluster_subscriptions_user_id")),
    )
    op.create_index(op.f("ix_cluster_subscriptions_cluster_id"), "cluster_subscriptions", ["cluster_id"], unique=False)
    op.create_index(op.f("ix_cluster_subscriptions_user_id"), "cluster_subscriptions", ["user_id"], unique=False)
    op.create_table(
        "discussion_subscriptions",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("discussion_id", sa.BigInteger(), nullable=False),
        sa.Column("joined", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("left", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["discussion_id"], ["discussions.id"], name=op.f("fk_discussion_subscriptions_discussion_id_discussions")
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name=op.f("fk_discussion_subscriptions_user_id_users")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_discussion_subscriptions")),
        sa.UniqueConstraint("discussion_id", "user_id", name=op.f("uq_discussion_subscriptions_discussion_id")),
    )
    op.create_index(
        op.f("ix_discussion_subscriptions_discussion_id"), "discussion_subscriptions", ["discussion_id"], unique=False
    )
    op.create_index(op.f("ix_discussion_subscriptions_user_id"), "discussion_subscriptions", ["user_id"], unique=False)
    op.create_table(
        "events",
        sa.Column("id", sa.BigInteger(), sa.Sequence("communities_seq"), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("content", sa.String(), nullable=False),
        sa.Column("thread_id", sa.BigInteger(), nullable=False),
        sa.Column(
            "geom",
            geoalchemy2.types.Geometry(geometry_type="POINT", srid=4326, from_text="ST_GeomFromEWKT", name="geometry"),
            nullable=False,
        ),
        sa.Column("address", sa.String(), nullable=False),
        sa.Column("photo", sa.String(), nullable=False),
        sa.Column("start_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("end_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("owner_user_id", sa.BigInteger(), nullable=False),
        sa.Column("owner_cluster_id", sa.BigInteger(), nullable=False),
        sa.ForeignKeyConstraint(
            ["owner_cluster_id"], ["clusters.id"], name=op.f("fk_events_owner_cluster_id_clusters")
        ),
        sa.ForeignKeyConstraint(["owner_user_id"], ["users.id"], name=op.f("fk_events_owner_user_id_users")),
        sa.ForeignKeyConstraint(["thread_id"], ["threads.id"], name=op.f("fk_events_thread_id_threads")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_events")),
    )
    op.create_index(op.f("ix_events_owner_cluster_id"), "events", ["owner_cluster_id"], unique=True)
    op.create_index(op.f("ix_events_owner_user_id"), "events", ["owner_user_id"], unique=False)
    op.create_index(op.f("ix_events_thread_id"), "events", ["thread_id"], unique=True)
    op.create_table(
        "node_cluster_associations",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("node_id", sa.BigInteger(), nullable=False),
        sa.Column("cluster_id", sa.BigInteger(), nullable=False),
        sa.ForeignKeyConstraint(
            ["cluster_id"], ["clusters.id"], name=op.f("fk_node_cluster_associations_cluster_id_clusters")
        ),
        sa.ForeignKeyConstraint(["node_id"], ["nodes.id"], name=op.f("fk_node_cluster_associations_node_id_nodes")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_node_cluster_associations")),
        sa.UniqueConstraint("node_id", "cluster_id", name=op.f("uq_node_cluster_associations_node_id")),
    )
    op.create_index(
        op.f("ix_node_cluster_associations_cluster_id"), "node_cluster_associations", ["cluster_id"], unique=False
    )
    op.create_index(
        op.f("ix_node_cluster_associations_node_id"), "node_cluster_associations", ["node_id"], unique=False
    )
    op.create_table(
        "pages",
        sa.Column("id", sa.BigInteger(), sa.Sequence("communities_seq"), nullable=False),
        sa.Column("type", sa.Enum("main_page", "point_of_interest", "guide", name="pagetype"), nullable=False),
        sa.Column("thread_id", sa.BigInteger(), nullable=True),
        sa.Column("creator_user_id", sa.BigInteger(), nullable=False),
        sa.Column("owner_user_id", sa.BigInteger(), nullable=True),
        sa.Column("owner_cluster_id", sa.BigInteger(), nullable=True),
        sa.Column("main_page_for_cluster_id", sa.BigInteger(), nullable=True),
        sa.ForeignKeyConstraint(["creator_user_id"], ["users.id"], name=op.f("fk_pages_creator_user_id_users")),
        sa.ForeignKeyConstraint(
            ["main_page_for_cluster_id"], ["clusters.id"], name=op.f("fk_pages_main_page_for_cluster_id_clusters")
        ),
        sa.ForeignKeyConstraint(["owner_cluster_id"], ["clusters.id"], name=op.f("fk_pages_owner_cluster_id_clusters")),
        sa.ForeignKeyConstraint(["owner_user_id"], ["users.id"], name=op.f("fk_pages_owner_user_id_users")),
        sa.ForeignKeyConstraint(["thread_id"], ["threads.id"], name=op.f("fk_pages_thread_id_threads")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_pages")),
    )
    op.create_index(op.f("ix_pages_creator_user_id"), "pages", ["creator_user_id"], unique=False)
    op.create_index(op.f("ix_pages_main_page_for_cluster_id"), "pages", ["main_page_for_cluster_id"], unique=True)
    op.create_index(op.f("ix_pages_owner_cluster_id"), "pages", ["owner_cluster_id"], unique=False)
    op.create_index(op.f("ix_pages_owner_user_id"), "pages", ["owner_user_id"], unique=False)
    op.create_index(op.f("ix_pages_thread_id"), "pages", ["thread_id"], unique=True)
    op.create_table(
        "replies",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("comment_id", sa.BigInteger(), nullable=False),
        sa.Column("author_user_id", sa.BigInteger(), nullable=False),
        sa.Column("content", sa.String(), nullable=False),
        sa.Column("created", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("deleted", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["author_user_id"], ["users.id"], name=op.f("fk_replies_author_user_id_users")),
        sa.ForeignKeyConstraint(["comment_id"], ["comments.id"], name=op.f("fk_replies_comment_id_comments")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_replies")),
    )
    op.create_index(op.f("ix_replies_comment_id"), "replies", ["comment_id"], unique=False)
    op.create_table(
        "cluster_event_associations",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("event_id", sa.BigInteger(), nullable=False),
        sa.Column("cluster_id", sa.BigInteger(), nullable=False),
        sa.ForeignKeyConstraint(
            ["cluster_id"], ["clusters.id"], name=op.f("fk_cluster_event_associations_cluster_id_clusters")
        ),
        sa.ForeignKeyConstraint(
            ["event_id"], ["events.id"], name=op.f("fk_cluster_event_associations_event_id_events")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_cluster_event_associations")),
        sa.UniqueConstraint("event_id", "cluster_id", name=op.f("uq_cluster_event_associations_event_id")),
    )
    op.create_index(
        op.f("ix_cluster_event_associations_cluster_id"), "cluster_event_associations", ["cluster_id"], unique=False
    )
    op.create_index(
        op.f("ix_cluster_event_associations_event_id"), "cluster_event_associations", ["event_id"], unique=False
    )
    op.create_table(
        "cluster_page_associations",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("page_id", sa.BigInteger(), nullable=False),
        sa.Column("cluster_id", sa.BigInteger(), nullable=False),
        sa.ForeignKeyConstraint(
            ["cluster_id"], ["clusters.id"], name=op.f("fk_cluster_page_associations_cluster_id_clusters")
        ),
        sa.ForeignKeyConstraint(["page_id"], ["pages.id"], name=op.f("fk_cluster_page_associations_page_id_pages")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_cluster_page_associations")),
        sa.UniqueConstraint("page_id", "cluster_id", name=op.f("uq_cluster_page_associations_page_id")),
    )
    op.create_index(
        op.f("ix_cluster_page_associations_cluster_id"), "cluster_page_associations", ["cluster_id"], unique=False
    )
    op.create_index(
        op.f("ix_cluster_page_associations_page_id"), "cluster_page_associations", ["page_id"], unique=False
    )
    op.create_table(
        "event_subscriptions",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("event_id", sa.BigInteger(), nullable=False),
        sa.Column("joined", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["event_id"], ["events.id"], name=op.f("fk_event_subscriptions_event_id_events")),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name=op.f("fk_event_subscriptions_user_id_users")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_event_subscriptions")),
        sa.UniqueConstraint("event_id", "user_id", name=op.f("uq_event_subscriptions_event_id")),
    )
    op.create_index(op.f("ix_event_subscriptions_event_id"), "event_subscriptions", ["event_id"], unique=False)
    op.create_index(op.f("ix_event_subscriptions_user_id"), "event_subscriptions", ["user_id"], unique=False)
    op.create_table(
        "page_versions",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("page_id", sa.BigInteger(), nullable=False),
        sa.Column("editor_user_id", sa.BigInteger(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("content", sa.String(), nullable=False),
        sa.Column("address", sa.String(), nullable=True),
        sa.Column(
            "geom",
            geoalchemy2.types.Geometry(geometry_type="POINT", srid=4326, from_text="ST_GeomFromEWKT", name="geometry"),
            nullable=True,
        ),
        sa.Column("created", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["editor_user_id"], ["users.id"], name=op.f("fk_page_versions_editor_user_id_users")),
        sa.ForeignKeyConstraint(["page_id"], ["pages.id"], name=op.f("fk_page_versions_page_id_pages")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_page_versions")),
    )
    op.create_index(op.f("ix_page_versions_editor_user_id"), "page_versions", ["editor_user_id"], unique=False)
    op.create_index(op.f("ix_page_versions_page_id"), "page_versions", ["page_id"], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_page_versions_page_id"), table_name="page_versions")
    op.drop_index(op.f("ix_page_versions_editor_user_id"), table_name="page_versions")
    op.drop_table("page_versions")
    op.drop_index(op.f("ix_event_subscriptions_user_id"), table_name="event_subscriptions")
    op.drop_index(op.f("ix_event_subscriptions_event_id"), table_name="event_subscriptions")
    op.drop_table("event_subscriptions")
    op.drop_index(op.f("ix_cluster_page_associations_page_id"), table_name="cluster_page_associations")
    op.drop_index(op.f("ix_cluster_page_associations_cluster_id"), table_name="cluster_page_associations")
    op.drop_table("cluster_page_associations")
    op.drop_index(op.f("ix_cluster_event_associations_event_id"), table_name="cluster_event_associations")
    op.drop_index(op.f("ix_cluster_event_associations_cluster_id"), table_name="cluster_event_associations")
    op.drop_table("cluster_event_associations")
    op.drop_index(op.f("ix_replies_comment_id"), table_name="replies")
    op.drop_table("replies")
    op.drop_index(op.f("ix_pages_thread_id"), table_name="pages")
    op.drop_index(op.f("ix_pages_owner_user_id"), table_name="pages")
    op.drop_index(op.f("ix_pages_owner_cluster_id"), table_name="pages")
    op.drop_index(op.f("ix_pages_main_page_for_cluster_id"), table_name="pages")
    op.drop_index(op.f("ix_pages_creator_user_id"), table_name="pages")
    op.drop_table("pages")
    op.drop_index(op.f("ix_node_cluster_associations_node_id"), table_name="node_cluster_associations")
    op.drop_index(op.f("ix_node_cluster_associations_cluster_id"), table_name="node_cluster_associations")
    op.drop_table("node_cluster_associations")
    op.drop_index(op.f("ix_events_thread_id"), table_name="events")
    op.drop_index(op.f("ix_events_owner_user_id"), table_name="events")
    op.drop_index(op.f("ix_events_owner_cluster_id"), table_name="events")
    op.drop_table("events")
    op.drop_index(op.f("ix_discussion_subscriptions_user_id"), table_name="discussion_subscriptions")
    op.drop_index(op.f("ix_discussion_subscriptions_discussion_id"), table_name="discussion_subscriptions")
    op.drop_table("discussion_subscriptions")
    op.drop_index(op.f("ix_cluster_subscriptions_user_id"), table_name="cluster_subscriptions")
    op.drop_index(op.f("ix_cluster_subscriptions_cluster_id"), table_name="cluster_subscriptions")
    op.drop_table("cluster_subscriptions")
    op.drop_index(
        op.f("ix_cluster_discussion_associations_discussion_id"), table_name="cluster_discussion_associations"
    )
    op.drop_index(op.f("ix_cluster_discussion_associations_cluster_id"), table_name="cluster_discussion_associations")
    op.drop_table("cluster_discussion_associations")
    op.drop_index(op.f("ix_discussions_thread_id"), table_name="discussions")
    op.drop_table("discussions")
    op.drop_index(op.f("ix_comments_thread_id"), table_name="comments")
    op.drop_table("comments")
    op.drop_index(op.f("ix_clusters_parent_node_id"), table_name="clusters")
    op.drop_index(op.f("ix_clusters_official_cluster_for_node_id"), table_name="clusters")
    op.drop_table("clusters")
    op.drop_table("threads")
    op.drop_index(op.f("ix_nodes_parent_node_id"), table_name="nodes")
    op.drop_table("nodes")
    # ### end Alembic commands ###
