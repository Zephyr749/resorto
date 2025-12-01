from modules.db.mongo_client import MongoDBClient
from modules.db.booking_schemas import SpotCreate, SpotUpdate, BookingCreate, BookingUpdate
from bson import ObjectId
from datetime import datetime
from typing import List, Optional

class BookingRepository:
    def __init__(self):
        self.db = MongoDBClient.get_instance().get_db()
        self.spots = self.db.spots
        self.bookings = self.db.bookings

    # Spot operations
    def createSpot(self, spot: SpotCreate) -> str:
        spot_dict = spot.dict()
        spot_dict['createdAt'] = datetime.utcnow()
        spot_dict['updatedAt'] = datetime.utcnow()
        result = self.spots.insert_one(spot_dict)
        return str(result.inserted_id)

    def getSpotById(self, spot_id: str) -> Optional[dict]:
        try:
            return self.spots.find_one({'_id': ObjectId(spot_id)})
        except:
            return None

    def getAllSpots(self, is_active: Optional[bool] = None, spot_type: Optional[str] = None) -> List[dict]:
        query = {}
        if is_active is not None:
            query['isActive'] = is_active
        if spot_type:
            query['spotType'] = spot_type
        return list(self.spots.find(query))

    def updateSpot(self, spot_id: str, spot_update: SpotUpdate) -> bool:
        update_data = {k: v for k, v in spot_update.dict(exclude_unset=True).items() if v is not None}
        if not update_data:
            return False
        
        update_data['updatedAt'] = datetime.utcnow()
        result = self.spots.update_one(
            {'_id': ObjectId(spot_id)},
            {'$set': update_data}
        )
        return result.modified_count > 0

    def deleteSpot(self, spot_id: str) -> bool:
        # Soft delete - just mark as inactive
        result = self.spots.update_one(
            {'_id': ObjectId(spot_id)},
            {'$set': {'isActive': False, 'updatedAt': datetime.utcnow()}}
        )
        return result.modified_count > 0

    # Booking operations
    def createBooking(self, booking: BookingCreate, user_id: str, total_amount: float) -> str:
        booking_dict = booking.dict()
        booking_dict['userId'] = user_id
        booking_dict['status'] = 'pending'
        booking_dict['paymentStatus'] = 'pending'
        booking_dict['totalAmount'] = total_amount
        booking_dict['createdAt'] = datetime.utcnow()
        booking_dict['updatedAt'] = datetime.utcnow()
        result = self.bookings.insert_one(booking_dict)
        return str(result.inserted_id)

    def getBookingById(self, booking_id: str) -> Optional[dict]:
        try:
            return self.bookings.find_one({'_id': ObjectId(booking_id)})
        except:
            return None

    def getUserBookings(self, user_id: str) -> List[dict]:
        return list(self.bookings.find({'userId': user_id}).sort('createdAt', -1))

    def getAllBookings(self, status: Optional[str] = None) -> List[dict]:
        query = {}
        if status:
            query['status'] = status
        return list(self.bookings.find(query).sort('createdAt', -1))

    def updateBooking(self, booking_id: str, booking_update: BookingUpdate) -> bool:
        update_data = {k: v for k, v in booking_update.dict(exclude_unset=True).items() if v is not None}
        if not update_data:
            return False
        
        update_data['updatedAt'] = datetime.utcnow()
        result = self.bookings.update_one(
            {'_id': ObjectId(booking_id)},
            {'$set': update_data}
        )
        return result.modified_count > 0

    def updateBookingStatus(self, booking_id: str, status: str) -> bool:
        result = self.bookings.update_one(
            {'_id': ObjectId(booking_id)},
            {'$set': {'status': status, 'updatedAt': datetime.utcnow()}}
        )
        return result.modified_count > 0

    def updatePaymentStatus(self, booking_id: str, payment_status: str, payment_id: Optional[str] = None) -> bool:
        update_data = {
            'paymentStatus': payment_status,
            'updatedAt': datetime.utcnow()
        }
        if payment_id:
            update_data['paymentId'] = payment_id
        
        result = self.bookings.update_one(
            {'_id': ObjectId(booking_id)},
            {'$set': update_data}
        )
        return result.modified_count > 0

    def getConflictingBookings(self, spot_id: str, check_in: datetime, check_out: datetime, exclude_booking_id: Optional[str] = None) -> List[dict]:
        """
        Find bookings that conflict with the given date range.
        A conflict occurs when:
        - The booking is for the same spot
        - The booking is not cancelled
        - The date ranges overlap
        """
        query = {
            'spotId': spot_id,
            'status': {'$nin': ['cancelled']},
            '$or': [
                # New booking starts during existing booking
                {'checkInDate': {'$lte': check_in}, 'checkOutDate': {'$gt': check_in}},
                # New booking ends during existing booking
                {'checkInDate': {'$lt': check_out}, 'checkOutDate': {'$gte': check_out}},
                # New booking contains existing booking
                {'checkInDate': {'$gte': check_in}, 'checkOutDate': {'$lte': check_out}}
            ]
        }
        
        if exclude_booking_id:
            query['_id'] = {'$ne': ObjectId(exclude_booking_id)}
        
        return list(self.bookings.find(query))

    def getBookingStats(self) -> dict:
        """Get booking statistics for admin dashboard"""
        pipeline = [
            {
                '$group': {
                    '_id': '$status',
                    'count': {'$sum': 1},
                    'revenue': {
                        '$sum': {
                            '$cond': [
                                {'$eq': ['$paymentStatus', 'paid']},
                                '$totalAmount',
                                0
                            ]
                        }
                    }
                }
            }
        ]
        
        stats = list(self.bookings.aggregate(pipeline))
        
        result = {
            'totalBookings': 0,
            'confirmedBookings': 0,
            'pendingBookings': 0,
            'cancelledBookings': 0,
            'totalRevenue': 0.0
        }
        
        for stat in stats:
            status = stat['_id']
            count = stat['count']
            revenue = stat['revenue']
            
            result['totalBookings'] += count
            result['totalRevenue'] += revenue
            
            if status == 'confirmed':
                result['confirmedBookings'] = count
            elif status == 'pending':
                result['pendingBookings'] = count
            elif status == 'cancelled':
                result['cancelledBookings'] = count
        
        # Today's bookings
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        result['todayBookings'] = self.bookings.count_documents({
            'createdAt': {'$gte': today_start}
        })
        
        return result
