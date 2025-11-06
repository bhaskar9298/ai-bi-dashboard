"""Utility package initializer"""
from .mongo_connector import mongo_connector, ReconciliationMongoConnector

# Backward compatibility alias
MongoConnector = ReconciliationMongoConnector

__all__ = ['mongo_connector', 'MongoConnector', 'ReconciliationMongoConnector']
