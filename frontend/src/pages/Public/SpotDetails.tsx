import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { message, Spin } from 'antd';
import { spotsApi } from '../../api/spots';
import { Spot } from '../../types';
import { useAuth } from '../../context/AuthContext';

const SpotDetails = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { user } = useAuth();
  const [spot, setSpot] = useState<Spot | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (id) {
      fetchSpot(id);
    }
  }, [id]);

  const fetchSpot = async (spotId: string) => {
    try {
      setLoading(true);
      const data = await spotsApi.getById(spotId);
      setSpot(data);
    } catch (error: any) {
      message.error('Failed to load spot details');
      navigate('/spots');
    } finally {
      setLoading(false);
    }
  };

  const handleBookNow = () => {
    if (!user) {
      message.info('Please login to book this spot');
      navigate('/login');
      return;
    }
    navigate(`/book/${spot?.id}`);
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Spin size="large" />
      </div>
    );
  }

  if (!spot) {
    return null;
  }

  return (
    <div className="py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-5xl mx-auto">
        {/* Back Button */}
        <button
          onClick={() => navigate('/spots')}
          className="mb-6 text-stone-600 hover:text-emerald-600 font-medium transition-colors"
        >
          ← Back to Spots
        </button>

        {/* Main Content */}
        <div className="glass-card overflow-hidden">
          {/* Image Gallery */}
          <div className="h-96 bg-gradient-to-br from-emerald-100 to-teal-100 flex items-center justify-center">
            {spot.images && spot.images[0] ? (
              <img 
                src={spot.images[0]} 
                alt={spot.name}
                className="w-full h-full object-cover"
              />
            ) : (
              <span className="text-8xl">{spot.spotType === 'picnic_area' ? '🏞️' : '🏨'}</span>
            )}
          </div>

          <div className="p-8">
            {/* Header */}
            <div className="flex items-start justify-between mb-6">
              <div>
                <span className="inline-block px-3 py-1 bg-emerald-100 text-emerald-700 text-sm font-semibold rounded-full mb-3">
                  {spot.spotType === 'picnic_area' ? 'Picnic Area' : 'Room'}
                </span>
                <h1 className="text-4xl font-bold text-stone-900 mb-2">
                  {spot.name}
                </h1>
                <p className="text-stone-600">
                  Perfect for up to {spot.capacity} guests
                </p>
              </div>
              <div className="text-right">
                <p className="text-4xl font-bold text-emerald-600">
                  ₹{spot.pricePerDay}
                </p>
                <p className="text-sm text-stone-500">per day</p>
              </div>
            </div>

            {/* Description */}
            <div className="mb-8">
              <h2 className="text-2xl font-bold text-stone-900 mb-3">About this spot</h2>
              <p className="text-stone-600 leading-relaxed">
                {spot.description}
              </p>
            </div>

            {/* Amenities */}
            {spot.amenities && spot.amenities.length > 0 && (
              <div className="mb-8">
                <h2 className="text-2xl font-bold text-stone-900 mb-4">Amenities</h2>
                <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                  {spot.amenities.map((amenity, idx) => (
                    <div key={idx} className="flex items-center space-x-2 bg-stone-50 px-4 py-3 rounded-lg">
                      <span className="text-emerald-600">✓</span>
                      <span className="text-stone-700">{amenity}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Booking Section */}
            <div className="pt-6 border-t border-stone-200">
              <div className="flex flex-col sm:flex-row gap-4">
                <button
                  onClick={handleBookNow}
                  className="btn-primary flex-1"
                >
                  Book This Spot
                </button>
                <button
                  onClick={() => navigate('/spots')}
                  className="flex-1 px-4 py-3 rounded-lg bg-stone-100 text-stone-700 font-semibold hover:bg-stone-200 transition-colors"
                >
                  View Other Spots
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SpotDetails;
