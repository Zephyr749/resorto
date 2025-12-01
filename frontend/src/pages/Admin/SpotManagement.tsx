import { useEffect, useState } from 'react';
import { message, Spin, Modal, Form, Input, InputNumber, Select } from 'antd';
import { adminApi } from '../../api/admin';
import { Spot, SpotCreate } from '../../types';

const { TextArea } = Input;
const { Option } = Select;

const SpotManagement = () => {
  const [spots, setSpots] = useState<Spot[]>([]);
  const [loading, setLoading] = useState(true);
  const [modalVisible, setModalVisible] = useState(false);
  const [editingSpot, setEditingSpot] = useState<Spot | null>(null);
  const [form] = Form.useForm();

  useEffect(() => {
    fetchSpots();
  }, []);

  const fetchSpots = async () => {
    try {
      setLoading(true);
      const data = await adminApi.getAllSpots();
      setSpots(data);
    } catch (error: any) {
      message.error('Failed to load spots');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateOrUpdate = async (values: any) => {
    try {
      const spotData: SpotCreate = {
        name: values.name,
        description: values.description,
        spotType: values.spotType,
        capacity: values.capacity,
        pricePerDay: values.pricePerDay,
        amenities: values.amenities ? values.amenities.split(',').map((a: string) => a.trim()) : [],
        images: values.images ? values.images.split(',').map((i: string) => i.trim()) : [],
      };

      if (editingSpot) {
        await adminApi.updateSpot(editingSpot.id, spotData);
        message.success('Spot updated successfully');
      } else {
        await adminApi.createSpot(spotData);
        message.success('Spot created successfully');
      }

      setModalVisible(false);
      setEditingSpot(null);
      form.resetFields();
      fetchSpots();
    } catch (error: any) {
      message.error(error.response?.data?.error || 'Operation failed');
    }
  };

  const handleEdit = (spot: Spot) => {
    setEditingSpot(spot);
    form.setFieldsValue({
      ...spot,
      amenities: spot.amenities?.join(', '),
      images: spot.images?.join(', '),
    });
    setModalVisible(true);
  };

  const handleToggleActive = async (spot: Spot) => {
    try {
      const spotData: any = {
        name: spot.name,
        description: spot.description,
        spotType: spot.spotType,
        capacity: spot.capacity,
        pricePerDay: spot.pricePerDay,
        amenities: spot.amenities,
        images: spot.images,
        isActive: !spot.isActive
      };
      await adminApi.updateSpot(spot.id, spotData);
      message.success(`Spot ${!spot.isActive ? 'activated' : 'deactivated'}`);
      fetchSpots();
    } catch (error: any) {
      message.error('Failed to update spot status');
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Spin size="large" />
      </div>
    );
  }

  return (
    <div className="py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-stone-900">Manage Spots</h1>
          <button
            onClick={() => {
              setEditingSpot(null);
              form.resetFields();
              setModalVisible(true);
            }}
            className="px-6 py-3 bg-gradient-to-r from-emerald-600 to-teal-600 text-white font-semibold rounded-lg hover:from-emerald-500 hover:to-teal-500 transition-all shadow-md"
          >
            + Add New Spot
          </button>
        </div>

        {/* Spots List */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {spots.map((spot) => (
            <div key={spot.id} className="glass-card p-6">
              <div className="flex items-start justify-between mb-4">
                <h3 className="text-xl font-bold text-stone-900">{spot.name}</h3>
                <span className={`px-3 py-1 text-xs font-semibold rounded-full ${spot.isActive ? 'bg-emerald-100 text-emerald-700' : 'bg-red-100 text-red-700'}`}>
                  {spot.isActive ? 'Active' : 'Inactive'}
                </span>
              </div>

              <p className="text-stone-600 text-sm mb-4 line-clamp-2">{spot.description}</p>

              <div className="space-y-2 text-sm text-stone-600 mb-4">
                <p><span className="font-semibold">Type:</span> {spot.spotType === 'picnic_area' ? 'Picnic Area' : 'Room'}</p>
                <p><span className="font-semibold">Capacity:</span> {spot.capacity} guests</p>
                <p><span className="font-semibold">Price:</span> ₹{spot.pricePerDay}/day</p>
              </div>

              <div className="flex gap-2">
                <button
                  onClick={() => handleEdit(spot)}
                  className="flex-1 px-4 py-2 bg-stone-100 text-stone-700 font-semibold rounded-lg hover:bg-stone-200 transition-colors"
                >
                  Edit
                </button>
                <button
                  onClick={() => handleToggleActive(spot)}
                  className={`flex-1 px-4 py-2 font-semibold rounded-lg transition-colors ${
                    spot.isActive
                      ? 'bg-red-100 text-red-700 hover:bg-red-200'
                      : 'bg-emerald-100 text-emerald-700 hover:bg-emerald-200'
                  }`}
                >
                  {spot.isActive ? 'Deactivate' : 'Activate'}
                </button>
              </div>
            </div>
          ))}
        </div>

        {/* Create/Edit Modal */}
        <Modal
          title={editingSpot ? 'Edit Spot' : 'Create New Spot'}
          open={modalVisible}
          onCancel={() => {
            setModalVisible(false);
            setEditingSpot(null);
            form.resetFields();
          }}
          footer={null}
          width={600}
        >
          <Form
            form={form}
            layout="vertical"
            onFinish={handleCreateOrUpdate}
            className="mt-4"
          >
            <Form.Item
              name="name"
              label={<span className="text-sm font-semibold text-stone-900">Spot Name</span>}
              rules={[{ required: true, message: 'Please enter spot name' }]}
            >
              <Input className="input-field" />
            </Form.Item>

            <Form.Item
              name="description"
              label={<span className="text-sm font-semibold text-stone-900">Description</span>}
              rules={[{ required: true, message: 'Please enter description' }]}
            >
              <TextArea rows={3} className="input-field" />
            </Form.Item>

            <div className="grid grid-cols-2 gap-4">
              <Form.Item
                name="spotType"
                label={<span className="text-sm font-semibold text-stone-900">Type</span>}
                rules={[{ required: true, message: 'Please select type' }]}
              >
                <Select className="w-full">
                  <Option value="picnic_area">Picnic Area</Option>
                  <Option value="room">Room</Option>
                </Select>
              </Form.Item>

              <Form.Item
                name="capacity"
                label={<span className="text-sm font-semibold text-stone-900">Capacity</span>}
                rules={[{ required: true, message: 'Please enter capacity' }]}
              >
                <InputNumber min={1} className="w-full" />
              </Form.Item>
            </div>

            <Form.Item
              name="pricePerDay"
              label={<span className="text-sm font-semibold text-stone-900">Price Per Day (₹)</span>}
              rules={[{ required: true, message: 'Please enter price' }]}
            >
              <InputNumber min={0} className="w-full" />
            </Form.Item>

            <Form.Item
              name="amenities"
              label={<span className="text-sm font-semibold text-stone-900">Amenities (comma-separated)</span>}
            >
              <Input className="input-field" placeholder="WiFi, Parking, Pool" />
            </Form.Item>

            <Form.Item
              name="images"
              label={<span className="text-sm font-semibold text-stone-900">Image URLs (comma-separated)</span>}
            >
              <Input className="input-field" placeholder="https://..." />
            </Form.Item>

            <div className="flex gap-3">
              <button type="submit" className="btn-primary">
                {editingSpot ? 'Update Spot' : 'Create Spot'}
              </button>
              <button
                type="button"
                onClick={() => {
                  setModalVisible(false);
                  setEditingSpot(null);
                  form.resetFields();
                }}
                className="flex-1 px-4 py-3 rounded-lg bg-stone-100 text-stone-700 font-semibold hover:bg-stone-200 transition-colors"
              >
                Cancel
              </button>
            </div>
          </Form>
        </Modal>
      </div>
    </div>
  );
};

export default SpotManagement;
