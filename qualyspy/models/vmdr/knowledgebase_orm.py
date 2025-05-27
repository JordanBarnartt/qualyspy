import datetime

import sqlalchemy as sa
import sqlalchemy.orm as orm


class Base(orm.DeclarativeBase):
    metadata = sa.MetaData(schema="qualys_knowledgebase")


class ChangeLog(Base):
    __tablename__ = "change_log"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    changes_date: orm.Mapped[datetime.datetime]
    comments: orm.Mapped[str]

    vuln_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("vuln.qid"))
    vuln: orm.Mapped["Vuln"] = orm.relationship(back_populates="change_log_list")


class Discovery(Base):
    __tablename__ = "discovery"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    remote: orm.Mapped[bool]
    auth_type_list: orm.Mapped[list[str]] = orm.mapped_column(sa.ARRAY(sa.String))
    additional_info: orm.Mapped[str | None]

    vuln_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("vuln.qid"))
    vuln: orm.Mapped["Vuln"] = orm.relationship(back_populates="discovery")


class ThreatIntel(Base):
    __tablename__ = "threat_intel"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    threat_intel_id: orm.Mapped[str]
    value: orm.Mapped[str]

    vuln_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("vuln.qid"))
    vuln: orm.Mapped["Vuln"] = orm.relationship(back_populates="threat_intelligence")


class Attack(Base):
    __tablename__ = "attack"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    vector: orm.Mapped[str | None]
    complexity: orm.Mapped[str | None]

    cvss_v3_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("cvss_v3.id"))
    cvss_v3: orm.Mapped["CVSSv3"] = orm.relationship(back_populates="attack")


class CVSSv3Impact(Base):
    __tablename__ = "cvss_v3_impact"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    confidentiality: orm.Mapped[str | None]
    integrity: orm.Mapped[str | None]
    availability: orm.Mapped[str | None]

    cvss_v3_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("cvss_v3.id"))
    cvss_v3: orm.Mapped["CVSSv3"] = orm.relationship(back_populates="impact")


class CVSSImpact(Base):
    __tablename__ = "cvss_impact"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    confidentiality: orm.Mapped[str | None]
    integrity: orm.Mapped[str | None]
    availability: orm.Mapped[str | None]

    cvss_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("cvss.id"))
    cvss: orm.Mapped["CVSS"] = orm.relationship(back_populates="impact")


class Access(Base):
    __tablename__ = "access"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    vector: orm.Mapped[str | None]
    complexity: orm.Mapped[str | None]

    cvss_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("cvss.id"))
    cvss: orm.Mapped["CVSS"] = orm.relationship(back_populates="access")


class CVSSv3Base(Base):
    __tablename__ = "cvss_v3_base"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    source: orm.Mapped[str | None]
    value: orm.Mapped[str]

    cvss_v3_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("cvss_v3.id"))
    cvss_v3: orm.Mapped["CVSSv3"] = orm.relationship(back_populates="base")


class CVSSBase(Base):
    __tablename__ = "cvss_base"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    source: orm.Mapped[str | None]
    value: orm.Mapped[str]

    cvss_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("cvss.id"))
    cvss: orm.Mapped["CVSS"] = orm.relationship(back_populates="base")


class CVSSv3(Base):
    __tablename__ = "cvss_v3"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    base: orm.Mapped[CVSSv3Base | None] = orm.relationship(
        back_populates="cvss_v3", uselist=False
    )
    temporal: orm.Mapped[float | None]
    vector_string: orm.Mapped[str | None]
    cvss3_version: orm.Mapped[str | None]
    attack: orm.Mapped[Attack | None] = orm.relationship(
        back_populates="cvss_v3", uselist=False
    )
    impact: orm.Mapped[CVSSv3Impact | None] = orm.relationship(
        back_populates="cvss_v3", uselist=False
    )
    privileges_required: orm.Mapped[str | None]
    user_interaction: orm.Mapped[str | None]
    scope: orm.Mapped[str | None]
    exploit_code_maturity: orm.Mapped[str | None]
    remediation_level: orm.Mapped[str | None]
    report_confidence: orm.Mapped[str | None]

    vuln_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("vuln.qid"))
    vuln: orm.Mapped["Vuln"] = orm.relationship(back_populates="cvss_v3")


class CVSS(Base):
    __tablename__ = "cvss"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    base: orm.Mapped[CVSSBase | None] = orm.relationship(
        back_populates="cvss", uselist=False
    )
    temporal: orm.Mapped[float | None]
    vector_string: orm.Mapped[str | None]
    cvss3_version: orm.Mapped[str | None]
    access: orm.Mapped[Access | None] = orm.relationship(
        back_populates="cvss", uselist=False
    )
    impact: orm.Mapped[CVSSImpact | None] = orm.relationship(
        back_populates="cvss", uselist=False
    )
    authentication: orm.Mapped[str | None]
    exploitability: orm.Mapped[str | None]
    remediation_level: orm.Mapped[str | None]
    report_confidence: orm.Mapped[str | None]

    vuln_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("vuln.qid"))
    vuln: orm.Mapped["Vuln"] = orm.relationship(back_populates="cvss")


class MWInfo(Base):
    __tablename__ = "mw_info"

    mw_id: orm.Mapped[str] = orm.mapped_column(primary_key=True)
    mw_type: orm.Mapped[str | None]
    mw_platform: orm.Mapped[str | None]
    mw_alias: orm.Mapped[str | None]
    mw_rating: orm.Mapped[str | None]
    mw_link: orm.Mapped[str | None]

    mw_src_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("mw_src.id"))
    mw_src: orm.Mapped["MWSrc"] = orm.relationship(back_populates="mw_list")


class MWSrc(Base):
    __tablename__ = "mw_src"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    src_name: orm.Mapped[str]
    mw_list: orm.Mapped[list[MWInfo]] = orm.relationship(
        back_populates="mw_src", uselist=True
    )

    correlation_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("correlation.id"))
    correlation: orm.Mapped["Correlation"] = orm.relationship(back_populates="malware")


class Explt(Base):
    __tablename__ = "explt"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    ref: orm.Mapped[str]
    desc: orm.Mapped[str]
    link: orm.Mapped[str | None]

    explt_src_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("explt_src.id"))
    explt_src: orm.Mapped["ExpltSrc"] = orm.relationship(back_populates="explt_list")


class ExpltSrc(Base):
    __tablename__ = "explt_src"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    src_name: orm.Mapped[str | None]
    explt_list: orm.Mapped[list[Explt]] = orm.relationship(
        back_populates="explt_src", uselist=True
    )

    correlation_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("correlation.id"))
    correlation: orm.Mapped["Correlation"] = orm.relationship(back_populates="exploits")


class Correlation(Base):
    __tablename__ = "correlation"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    exploits: orm.Mapped[list[ExpltSrc]] = orm.relationship(
        back_populates="correlation", uselist=True
    )
    malware: orm.Mapped[list[MWSrc]] = orm.relationship(
        back_populates="correlation", uselist=True
    )

    vuln_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("vuln.qid"))
    vuln: orm.Mapped["Vuln"] = orm.relationship(back_populates="correlation")


class Compliance(Base):
    __tablename__ = "compliance"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    type: orm.Mapped[str]
    section: orm.Mapped[str]
    description: orm.Mapped[str]

    vuln_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("vuln.qid"))
    vuln: orm.Mapped["Vuln"] = orm.relationship(back_populates="compliance_list")


cve_association_table = sa.Table(
    "cve_association",
    Base.metadata,
    sa.Column("cve_id", sa.ForeignKey("cve.id")),
    sa.Column("vuln_qid", sa.ForeignKey("vuln.qid")),
)


class CVE(Base):
    __tablename__ = "cve"

    id: orm.Mapped[str] = orm.mapped_column(primary_key=True)
    url: orm.Mapped[str]

    vulns: orm.Mapped[list["Vuln"]] = orm.relationship(
        secondary=cve_association_table, back_populates="cve_list", uselist=True
    )


class VendorReference(Base):
    __tablename__ = "vendor_reference"

    id: orm.Mapped[str] = orm.mapped_column(primary_key=True)
    url: orm.Mapped[str]

    vuln_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("vuln.qid"))
    vuln: orm.Mapped["Vuln"] = orm.relationship(back_populates="vendor_reference_list")


class Software(Base):
    __tablename__ = "software"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    product: orm.Mapped[str]
    vendor: orm.Mapped[str]

    vuln_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("vuln.qid"))
    vuln: orm.Mapped["Vuln"] = orm.relationship(back_populates="software_list")


class Bugtraq(Base):
    __tablename__ = "bugtraq"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    bugtraq_id: orm.Mapped[str]
    url: orm.Mapped[str]

    vuln_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("vuln.qid"))
    vuln: orm.Mapped["Vuln"] = orm.relationship(back_populates="bugtraq_list")


class LastCustomization(Base):
    __tablename__ = "last_customization"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    last_customization_datetime: orm.Mapped[datetime.datetime | None]
    user_login: orm.Mapped[str | None]

    vuln_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("vuln.qid"))
    vuln: orm.Mapped["Vuln"] = orm.relationship(back_populates="last_customization")


class Vuln(Base):
    __tablename__ = "vuln"

    qid: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    vuln_type: orm.Mapped[str]
    severity_level: orm.Mapped[int]
    title: orm.Mapped[str]
    category: orm.Mapped[str | None]
    detection_info: orm.Mapped[str | None]
    last_customization: orm.Mapped[LastCustomization | None] = orm.relationship(
        back_populates="vuln", uselist=False
    )
    last_service_modification_datetime: orm.Mapped[datetime.datetime | None]
    published_datetime: orm.Mapped[datetime.datetime | None]
    code_modified_datetime: orm.Mapped[datetime.datetime | None]
    bugtraq_list: orm.Mapped[list[Bugtraq]] = orm.relationship(
        back_populates="vuln", uselist=True
    )
    patchable: orm.Mapped[bool | None]
    patch_published_date: orm.Mapped[datetime.datetime | None]
    software_list: orm.Mapped[list[Software]] = orm.relationship(
        back_populates="vuln", uselist=True
    )
    vendor_reference_list: orm.Mapped[list[VendorReference]] = orm.relationship(
        back_populates="vuln", uselist=True
    )
    cve_list: orm.Mapped[list[CVE]] = orm.relationship(
        secondary=cve_association_table, back_populates="vulns", uselist=True
    )
    diagnosis: orm.Mapped[str | None]
    diagnosis_comment: orm.Mapped[str | None]
    consequence: orm.Mapped[str | None]
    consequence_comment: orm.Mapped[str | None]
    solution: orm.Mapped[str | None]
    solution_comment: orm.Mapped[str | None]
    compliance_list: orm.Mapped[list[Compliance]] = orm.relationship(
        back_populates="vuln", uselist=True
    )
    correlation: orm.Mapped[Correlation | None] = orm.relationship(
        back_populates="vuln", uselist=False
    )
    cvss: orm.Mapped[CVSS | None] = orm.relationship(
        back_populates="vuln", uselist=False
    )
    cvss_v3: orm.Mapped[CVSSv3 | None] = orm.relationship(
        back_populates="vuln", uselist=False
    )
    pci_flag: orm.Mapped[bool | None]
    automatic_pci_fail: orm.Mapped[bool | None]
    pci_reasons: orm.Mapped[list[str]] = orm.mapped_column(sa.ARRAY(sa.String))
    threat_intelligence: orm.Mapped[list[ThreatIntel]] = orm.relationship(
        back_populates="vuln", uselist=True
    )
    supported_modules: orm.Mapped[str | None]
    discovery: orm.Mapped[Discovery | None] = orm.relationship(
        back_populates="vuln", uselist=False
    )
    is_disabled: orm.Mapped[bool | None]
    change_log_list: orm.Mapped[list[ChangeLog]] = orm.relationship(
        back_populates="vuln", uselist=True
    )
