# coding: utf-8
from sqlalchemy import DECIMAL, DateTime  # API Logic Server GenAI assist
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

########################################################################################################################
# Classes describing database for SqlAlchemy ORM, initially created by schema introspection.
#
# Alter this file per your database maintenance policy
#    See https://apilogicserver.github.io/Docs/Project-Rebuild/#rebuilding
#
# Created:  January 29, 2025 09:55:37
# Database: sqlite:////tmp/tmp.YizUFLElqp-01JJRQRGZ13SWAV3DFRXZ29G28/CMDBDatabase/database/db.sqlite
# Dialect:  sqlite
#
# mypy: ignore-errors
########################################################################################################################
 
from database.system.SAFRSBaseX import SAFRSBaseX, TestBase
from flask_login import UserMixin
import safrs, flask_sqlalchemy, os
from safrs import jsonapi_attr
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.sql.sqltypes import NullType
from typing import List

db = SQLAlchemy() 
Base = declarative_base()  # type: flask_sqlalchemy.model.DefaultMeta
metadata = Base.metadata

#NullType = db.String  # datatype fixup
#TIMESTAMP= db.TIMESTAMP

from sqlalchemy.dialects.sqlite import *

if os.getenv('APILOGICPROJECT_NO_FLASK') is None or os.getenv('APILOGICPROJECT_NO_FLASK') == 'None':
    Base = SAFRSBaseX   # enables rules to be used outside of Flask, e.g., test data loading
else:
    Base = TestBase     # ensure proper types, so rules work for data loading
    print('*** Models.py Using TestBase ***')



class DeviceType(Base):  # type: ignore
    """
    description: Different types of devices within the network.
    """
    __tablename__ = 'device_type'
    _s_collection_name = 'DeviceType'  # type: ignore

    id = Column(Integer, primary_key=True)
    type_name = Column(String)

    # parent relationships (access parent)

    # child relationships (access children)
    ConfigurationItemList : Mapped[List["ConfigurationItem"]] = relationship(back_populates="type")



class Location(Base):  # type: ignore
    """
    description: Represents a physical or logical location.
    """
    __tablename__ = 'location'
    _s_collection_name = 'Location'  # type: ignore

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    address = Column(String)

    # parent relationships (access parent)

    # child relationships (access children)
    ServerList : Mapped[List["Server"]] = relationship(back_populates="location")



class Vendor(Base):  # type: ignore
    """
    description: Information about software vendors.
    """
    __tablename__ = 'vendor'
    _s_collection_name = 'Vendor'  # type: ignore

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    # parent relationships (access parent)

    # child relationships (access children)
    ApplicationList : Mapped[List["Application"]] = relationship(back_populates="vendor")
    ConfigurationItemList : Mapped[List["ConfigurationItem"]] = relationship(back_populates="vendor")
    OperatingSystemList : Mapped[List["OperatingSystem"]] = relationship(back_populates="vendor")



class Application(Base):  # type: ignore
    """
    description: Details of applications including version and vendor.
    """
    __tablename__ = 'application'
    _s_collection_name = 'Application'  # type: ignore

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    version = Column(String)
    vendor_id = Column(ForeignKey('vendor.id'))

    # parent relationships (access parent)
    vendor : Mapped["Vendor"] = relationship(back_populates=("ApplicationList"))

    # child relationships (access children)



class ConfigurationItem(Base):  # type: ignore
    """
    description: Represents different configuration items related to devices.
    """
    __tablename__ = 'configuration_item'
    _s_collection_name = 'ConfigurationItem'  # type: ignore

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    type_id = Column(ForeignKey('device_type.id'))
    vendor_id = Column(ForeignKey('vendor.id'))

    # parent relationships (access parent)
    type : Mapped["DeviceType"] = relationship(back_populates=("ConfigurationItemList"))
    vendor : Mapped["Vendor"] = relationship(back_populates=("ConfigurationItemList"))

    # child relationships (access children)



class OperatingSystem(Base):  # type: ignore
    """
    description: Details about various operating systems used on servers.
    """
    __tablename__ = 'operating_system'
    _s_collection_name = 'OperatingSystem'  # type: ignore

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    version = Column(String)
    vendor_id = Column(ForeignKey('vendor.id'))

    # parent relationships (access parent)
    vendor : Mapped["Vendor"] = relationship(back_populates=("OperatingSystemList"))

    # child relationships (access children)



class Server(Base):  # type: ignore
    """
    description: Stores information about servers in the CMDB.
    """
    __tablename__ = 'server'
    _s_collection_name = 'Server'  # type: ignore

    id = Column(Integer, primary_key=True)
    hostname = Column(String, nullable=False)
    ip_address = Column(String, nullable=False)
    location_id = Column(ForeignKey('location.id'))

    # parent relationships (access parent)
    location : Mapped["Location"] = relationship(back_populates=("ServerList"))

    # child relationships (access children)
    IncidentList : Mapped[List["Incident"]] = relationship(back_populates="server")
    MaintenanceScheduleList : Mapped[List["MaintenanceSchedule"]] = relationship(back_populates="server")
    NetworkInterfaceList : Mapped[List["NetworkInterface"]] = relationship(back_populates="server")
    UserAccountList : Mapped[List["UserAccount"]] = relationship(back_populates="server")



class Incident(Base):  # type: ignore
    """
    description: Records incidents occurring on the server systems.
    """
    __tablename__ = 'incident'
    _s_collection_name = 'Incident'  # type: ignore

    id = Column(Integer, primary_key=True)
    description = Column(String)
    report_time = Column(DateTime)
    resolution_time = Column(DateTime)
    server_id = Column(ForeignKey('server.id'))

    # parent relationships (access parent)
    server : Mapped["Server"] = relationship(back_populates=("IncidentList"))

    # child relationships (access children)



class MaintenanceSchedule(Base):  # type: ignore
    """
    description: Scheduling of maintenance activities on servers.
    """
    __tablename__ = 'maintenance_schedule'
    _s_collection_name = 'MaintenanceSchedule'  # type: ignore

    id = Column(Integer, primary_key=True)
    server_id = Column(ForeignKey('server.id'))
    planned_date = Column(DateTime)

    # parent relationships (access parent)
    server : Mapped["Server"] = relationship(back_populates=("MaintenanceScheduleList"))

    # child relationships (access children)



class NetworkInterface(Base):  # type: ignore
    """
    description: Network interface cards for the servers.
    """
    __tablename__ = 'network_interface'
    _s_collection_name = 'NetworkInterface'  # type: ignore

    id = Column(Integer, primary_key=True)
    ip_address = Column(String, nullable=False)
    mac_address = Column(String, nullable=False)
    server_id = Column(ForeignKey('server.id'))

    # parent relationships (access parent)
    server : Mapped["Server"] = relationship(back_populates=("NetworkInterfaceList"))

    # child relationships (access children)



class UserAccount(Base):  # type: ignore
    """
    description: User accounts associated with servers.
    """
    __tablename__ = 'user_account'
    _s_collection_name = 'UserAccount'  # type: ignore

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    server_id = Column(ForeignKey('server.id'))

    # parent relationships (access parent)
    server : Mapped["Server"] = relationship(back_populates=("UserAccountList"))

    # child relationships (access children)
    AccessLogList : Mapped[List["AccessLog"]] = relationship(back_populates="user_account")



class AccessLog(Base):  # type: ignore
    """
    description: Tracks user logins and logouts.
    """
    __tablename__ = 'access_log'
    _s_collection_name = 'AccessLog'  # type: ignore

    id = Column(Integer, primary_key=True)
    user_account_id = Column(ForeignKey('user_account.id'))
    login_time = Column(DateTime)
    logout_time = Column(DateTime)

    # parent relationships (access parent)
    user_account : Mapped["UserAccount"] = relationship(back_populates=("AccessLogList"))

    # child relationships (access children)
