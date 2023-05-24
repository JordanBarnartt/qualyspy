import datetime as dt

import sqlalchemy.orm as orm


class Base(orm.DeclarativeBase):
    pass


class Attribute(Base):
    __tablename__ = "attribute"

    name: orm.Mapped[str] = orm.mapped_column(primary_key=True)
    last_status: orm.Mapped[str | None]
    value: orm.Mapped[str | None]
    last_success_date: orm.Mapped[dt.datetime | None]
    last_error_date: orm.Mapped[dt.datetime | None]
    last_error: orm.Mapped[str | None]
    provider: orm.Mapped["Azure" | "Ec2" | "Google" | None] = orm.relationship(
        back_populates="attribute"
    )


class CloudTag(Base):
    __tablename__ = "cloud_tag"

    name: orm.Mapped[str] = orm.mapped_column(primary_key=True)
    value: orm.Mapped[str | None]
    last_success_date: orm.Mapped[dt.datetime | None]
    cloud_provider_tags: orm.Mapped["CloudProviderTags"] = orm.relationship(
        back_populates="cloud_tag"
    )


class DnsData(Base):
    __tablename__ = "dns_data"

    hostname: orm.Mapped[str | None]
    domain: orm.Mapped[str | None]
    fqdn: orm.Mapped[str] = orm.mapped_column(primary_key=True)


class Param(Base):
    __tablename__ = "param"

    key: orm.Mapped[str] = orm.mapped_column(primary_key=True)
    value: orm.Mapped[str | None]
    param_list: orm.Mapped["ParamList"] = orm.relationship(back_populates="param")


class Qds(Base):
    __tablename__ = "qds"

    severity: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    value: orm.Mapped[int] = orm.mapped_column(primary_key=True)


class QdsFactor(Base):
    __tablename__ = "qds_factor"

    name: orm.Mapped[str] = orm.mapped_column(primary_key=True)
    value: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    qds_factors: orm.Mapped["QdsFactors"] = orm.relationship(
        back_populates="qds_factor"
    )


class Tag(Base):
    __tablename__ = "tag"

    tag_id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    name: orm.Mapped[str]
    color: orm.Mapped[str | None]
    background_color: orm.Mapped[str | None]


class Azure(Base):
    __tablename__ = "azure"

    attribute: orm.Mapped[list[Attribute]] = orm.relationship(back_populates="provider")


class CloudProviderTags:
    __tablename__ = "cloud_provider_tags"

    cloud_tag: orm.Mapped[list[CloudTag]] = orm.relationship(
        back_populates="cloud_provider_tags"
    )


class Ec2:
    __tablename__ = "ec2"

    attribute: orm.Mapped[list[Attribute]] = orm.relationship(back_populates="provider")


class Google:
    __tablename__ = "google"

    attribute: orm.Mapped[list[Attribute]] = orm.relationship(back_populates="provider")


class ParamList:
    __tablename__ = "param_list"

    param: orm.Mapped[list[Param]] = orm.relationship(back_populates="param_list")


class QdsFactors:
    __tablename__ = "qds_factors"

    qds_factor: orm.Mapped[list[QdsFactor]] = orm.relationship(
        back_populates="qds_factors"
    )
