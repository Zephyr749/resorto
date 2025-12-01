import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { message, Spin } from 'antd';
import { spotsApi } from '../../api/spots';
import { Spot } from '../../types';

const SpotList = () => {
  const [spots, setSpots] = useState<Spot[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<'all' | 'picnic_area' | 'room'>('all');

  useEffect(() => {
    fetchSpots();
  }, []);

  const fetchSpots = async () => {
    try {
      setLoading(true);
      const data = await spotsApi.getAll();
      setSpots(data);
    } catch (error: any) {
      message.error('Failed to load spots');
    } finally {
      setLoading(false);
    }
  };

  const filteredSpots = spots.filter(spot => {
    if (filter === 'all') return spot.isActive;
    return spot.isActive && spot.spotType === filter;
  });

  return (
    <div className="py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        {/* Hero Section */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-stone-900 mb-4">
            Discover Our Resort Spots
          </h1>
          <p className="text-lg text-stone-600 max-w-2xl mx-auto">
            Find the perfect spot for your next getaway. From peaceful picnic areas to luxurious rooms.
          </p>
        </div>

        {/* Filter Tabs */}
        <div className="flex justify-center gap-4 mb-8">
          <button
            onClick={() => setFilter('all')}
            className={`px-6 py-2 rounded-lg font-medium transition-all ${
              filter === 'all'
                ? 'bg-gradient-to-r from-emerald-600 to-teal-600 text-white shadow-md'
                : 'bg-white text-stone-700 hover:bg-stone-50'
            }`}
          >
            All Spots
          </button>
          <button
            onClick={() => setFilter('picnic_area')}
            className={`px-6 py-2 rounded-lg font-medium transition-all ${
              filter === 'picnic_area'
                ? 'bg-gradient-to-r from-emerald-600 to-teal-600 text-white shadow-md'
                : 'bg-white text-stone-700 hover:bg-stone-50'
            }`}
          >
            Picnic Areas
          </button>
          <button
            onClick={() => setFilter('room')}
            className={`px-6 py-2 rounded-lg font-medium transition-all ${
              filter === 'room'
                ? 'bg-gradient-to-r from-emerald-600 to-teal-600 text-white shadow-md'
                : 'bg-white text-stone-700 hover:bg-stone-50'
            }`}
          >
            Rooms
          </button>
        </div>

        {/* Loading State */}
        {loading && (
          <div className="text-center py-20">
            <Spin size="large" />
            <p className="mt-4 text-stone-600">Loading amazing spots...</p>
          </div>
        )}

        {/* Empty State */}
        {!loading && filteredSpots.length === 0 && (
          <div className="glass-card p-12 text-center">
            <div className="text-6xl mb-6">🏖️</div>
            <h2 className="text-2xl font-semibold text-stone-900 mb-4">
              No Spots Available
            </h2>
            <p className="text-stone-600">
              {filter === 'all' 
                ? "We're preparing amazing spots for you. Check back soon!"
                : `No ${filter === 'picnic_area' ? 'picnic areas' : 'rooms'} available at the moment.`
              }
            </p>
          </div>
        )}

        {/* Spots Grid */}
        {!loading && filteredSpots.length > 0 && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredSpots.map((spot) => (
              <Link
                key={spot.id}
                to={`/spots/${spot.id}`}
                className="glass-card overflow-hidden hover:shadow-2xl transition-all duration-300 group"
              >
                {/* Image */}
                <div className="h-48 bg-gradient-to-br from-emerald-100 to-teal-100 flex items-center justify-center overflow-hidden">
                  {spot.images && spot.images[0] ? (
                    <img 
                      src={spot.images[0]} 
                      alt={spot.name}
                      className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300"
                    />
                  ) : (
                    <span className="text-6xl">{spot.spotType === 'picnic_area' ? '🏞️' : '🏨'}</span>
                  )}
                </div>

                {/* Content */}
                <div className="p-6">
                  <div className="flex items-start justify-between mb-2">
                    <h3 className="text-xl font-bold text-stone-900 group-hover:text-emerald-600 transition-colors">
                      {spot.name}
                    </h3>
                    <span className="px-3 py-1 bg-emerald-100 text-emerald-700 text-xs font-semibold rounded-full">
                      {spot.spotType === 'picnic_area' ? 'Picnic' : 'Room'}
                    </span>
                  </div>

                  <p className="text-stone-600 text-sm mb-4 line-clamp-2">
                    {spot.description}
                  </p>

                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-2xl font-bold text-emerald-600">
                        ₹{spot.pricePerDay}
                      </p>
                      <p className="text-xs text-stone-500">per day</p>
                    </div>
                    <div className="text-right">
                      <p className="text-sm text-stone-600">
                        Up to {spot.capacity} guests
                      </p>
                    </div>
                  </div>

                  {/* Amenities Preview */}
                  {spot.amenities && spot.amenities.length > 0 && (
                    <div className="mt-4 pt-4 border-t border-stone-200">
                      <div className="flex flex-wrap gap-2">
                        {spot.amenities.slice(0, 3).map((amenity, idx) => (
                          <span key={idx} className="text-xs bg-stone-100 text-stone-700 px-2 py-1 rounded">
                            {amenity}
                          </span>
                        ))}
                        {spot.amenities.length > 3 && (
                          <span className="text-xs text-stone-500">
                            +{spot.amenities.length - 3} more
                          </span>
                        )}
                      </div>
                    </div>
                  )}
                </div>
              </Link>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default SpotList;
