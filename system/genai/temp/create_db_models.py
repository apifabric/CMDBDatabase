# using resolved_model self.resolved_model FIXME
# created from response, to create create_db_models.sqlite, with test data
#    that is used to create project
# should run without error in manager 
#    if not, check for decimal, indent, or import issues

import decimal
import logging
import sqlalchemy
from sqlalchemy.sql import func 
from decimal import Decimal
from logic_bank.logic_bank import Rule
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Date, DateTime, Numeric, Boolean, Text, DECIMAL
from sqlalchemy.types import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from datetime import date   
from datetime import datetime
from typing import List


logging.getLogger('sqlalchemy.engine.Engine').disabled = True  # remove for additional logging

Base = declarative_base()  # from system/genai/create_db_models_inserts/create_db_models_prefix.py


from sqlalchemy.dialects.sqlite import *

class Server(Base):
    """description: Stores information about servers in the CMDB."""
    __tablename__ = 'server'
    id = Column(Integer, primary_key=True, autoincrement=True)
    hostname = Column(String, nullable=False)
    ip_address = Column(String, nullable=False)
    location_id = Column(Integer, ForeignKey('location.id'))

class Location(Base):
    """description: Represents a physical or logical location."""
    __tablename__ = 'location'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    address = Column(String)

class Application(Base):
    """description: Details of applications including version and vendor."""
    __tablename__ = 'application'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    version = Column(String)
    vendor_id = Column(Integer, ForeignKey('vendor.id'))

class Vendor(Base):
    """description: Information about software vendors."""
    __tablename__ = 'vendor'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)

class OperatingSystem(Base):
    """description: Details about various operating systems used on servers."""
    __tablename__ = 'operating_system'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    version = Column(String)
    vendor_id = Column(Integer, ForeignKey('vendor.id'))

class DeviceType(Base):
    """description: Different types of devices within the network."""
    __tablename__ = 'device_type'
    id = Column(Integer, primary_key=True, autoincrement=True)
    type_name = Column(String)

class ConfigurationItem(Base):
    """description: Represents different configuration items related to devices."""
    __tablename__ = 'configuration_item'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    type_id = Column(Integer, ForeignKey('device_type.id'))
    vendor_id = Column(Integer, ForeignKey('vendor.id'))

class NetworkInterface(Base):
    """description: Network interface cards for the servers."""
    __tablename__ = 'network_interface'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ip_address = Column(String, nullable=False)
    mac_address = Column(String, nullable=False)
    server_id = Column(Integer, ForeignKey('server.id'))

class UserAccount(Base):
    """description: User accounts associated with servers."""
    __tablename__ = 'user_account'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False)
    server_id = Column(Integer, ForeignKey('server.id'))

class AccessLog(Base):
    """description: Tracks user logins and logouts."""
    __tablename__ = 'access_log'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_account_id = Column(Integer, ForeignKey('user_account.id'))
    login_time = Column(DateTime)
    logout_time = Column(DateTime)

class MaintenanceSchedule(Base):
    """description: Scheduling of maintenance activities on servers."""
    __tablename__ = 'maintenance_schedule'
    id = Column(Integer, primary_key=True, autoincrement=True)
    server_id = Column(Integer, ForeignKey('server.id'))
    planned_date = Column(DateTime)

class Incident(Base):
    """description: Records incidents occurring on the server systems."""
    __tablename__ = 'incident'
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String)
    report_time = Column(DateTime)
    resolution_time = Column(DateTime)
    server_id = Column(Integer, ForeignKey('server.id'))


# end of model classes


try:
    
    
    # ALS/GenAI: Create an SQLite database
    import os
    mgr_db_loc = True
    if mgr_db_loc:
        print(f'creating in manager: sqlite:///system/genai/temp/create_db_models.sqlite')
        engine = create_engine('sqlite:///system/genai/temp/create_db_models.sqlite')
    else:
        current_file_path = os.path.dirname(__file__)
        print(f'creating at current_file_path: {current_file_path}')
        engine = create_engine(f'sqlite:///{current_file_path}/create_db_models.sqlite')
    Base.metadata.create_all(engine)
    
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # ALS/GenAI: Prepare for sample data
    
    
    session.commit()
    server1 = Server(hostname="server01", ip_address="192.168.1.1", location_id=1)
    server2 = Server(hostname="server02", ip_address="192.168.1.2", location_id=2)
    server3 = Server(hostname="server03", ip_address="192.168.1.3", location_id=1)
    server4 = Server(hostname="server04", ip_address="192.168.1.4", location_id=2)
    location1 = Location(name="DataCenter 1", address="123 Main St.")
    location2 = Location(name="DataCenter 2", address="456 Side St.")
    location3 = Location(name="Remote Storage", address="789 Remote Rd.")
    location4 = Location(name="HQ Office", address="10 HQ Blvd.")
    
    
    
    session.add_all([server1, server2, server3, server4, location1, location2, location3, location4])
    session.commit()
    # end of test data
    
    
except Exception as exc:
    print(f'Test Data Error: {exc}')
