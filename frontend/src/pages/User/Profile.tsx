import { useState } from 'react';
import { Form, Input, Modal, message } from 'antd';
import { useAuth } from '../../context/AuthContext';
import { authApi } from '../../api/auth';

const Profile = () => {
  const { user, updateUser } = useAuth();
  const [editLoading, setEditLoading] = useState(false);
  const [passwordLoading, setPasswordLoading] = useState(false);
  const [editModalVisible, setEditModalVisible] = useState(false);
  const [passwordModalVisible, setPasswordModalVisible] = useState(false);
  const [editForm] = Form.useForm();
  const [passwordForm] = Form.useForm();

  const handleUpdateProfile = async (values: { firstName: string; lastName: string }) => {
    setEditLoading(true);
    try {
      const updatedUser = await authApi.updateProfile(values);
      updateUser(updatedUser);
      message.success('Profile updated successfully');
      setEditModalVisible(false);
      editForm.resetFields();
    } catch (error: any) {
      message.error(error.response?.data?.error || 'Failed to update profile');
    } finally {
      setEditLoading(false);
    }
  };

  const handleChangePassword = async (values: {
    currentPassword: string;
    newPassword: string;
  }) => {
    setPasswordLoading(true);
    try {
      await authApi.changePassword(values);
      message.success('Password changed successfully');
      setPasswordModalVisible(false);
      passwordForm.resetFields();
    } catch (error: any) {
      message.error(error.response?.data?.error || 'Failed to change password');
    } finally {
      setPasswordLoading(false);
    }
  };

  if (!user) return null;

  return (
    <div className="min-h-screen py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-3xl mx-auto">
        {/* Header with Avatar */}
        <div className="text-center mb-8">
          <div className="flex justify-center mb-4">
            <div className="w-24 h-24 bg-gradient-to-r from-emerald-600 to-teal-600 rounded-full flex items-center justify-center text-4xl text-white font-bold shadow-lg">
              {user.firstName?.[0]}{user.lastName?.[0]}
            </div>
          </div>
          <h1 className="text-3xl font-bold text-stone-900 mb-2">
            {user.fullName}
          </h1>
          <p className="text-stone-600 text-sm">
            {user.role === 'admin' ? '👑 Administrator' : '👤 User'}
          </p>
        </div>

        {/* Profile Information Card */}
        <div className="glass-card p-8 mb-6">
          <h2 className="text-xl font-semibold text-stone-900 mb-6">Profile Information</h2>
          
          <div className="space-y-6">
            <div>
              <label className="block text-sm font-semibold text-stone-700 mb-1">Email Address</label>
              <p className="text-stone-900 text-lg">{user.email}</p>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-semibold text-stone-700 mb-1">First Name</label>
                <p className="text-stone-900 text-lg">{user.firstName}</p>
              </div>
              <div>
                <label className="block text-sm font-semibold text-stone-700 mb-1">Last Name</label>
                <p className="text-stone-900 text-lg">{user.lastName}</p>
              </div>
            </div>
          </div>

          <div className="mt-8 flex flex-col sm:flex-row gap-6">
            <button
              onClick={() => {
                editForm.setFieldsValue({
                  firstName: user.firstName,
                  lastName: user.lastName,
                });
                setEditModalVisible(true);
              }}
              className="btn-primary"
            >
              Edit Profile
            </button>
            <button
              onClick={() => setPasswordModalVisible(true)}
              className="btn-secondary"
            >
              Change Password
            </button>
          </div>
        </div>

        {/* Edit Profile Modal */}
        <Modal
          title="Edit Profile"
          open={editModalVisible}
          onCancel={() => setEditModalVisible(false)}
          footer={null}
          width={500}
        >
          <Form
            form={editForm}
            layout="vertical"
            onFinish={handleUpdateProfile}
            className="mt-6"
          >
            <Form.Item
              name="firstName"
              label={<span className="text-sm font-semibold text-stone-900">First Name</span>}
              rules={[{ required: true, message: 'Please enter your first name' }]}
              className="mb-4"
            >
              <Input placeholder="Enter your first name" className="input-field" size="large" />
            </Form.Item>

            <Form.Item
              name="lastName"
              label={<span className="text-sm font-semibold text-stone-900">Last Name</span>}
              rules={[{ required: true, message: 'Please enter your last name' }]}
              className="mb-6"
            >
              <Input placeholder="Enter your last name" className="input-field" size="large" />
            </Form.Item>

            <div className="flex gap-3 justify-end mt-8">
              <button
                type="button"
                onClick={() => setEditModalVisible(false)}
                className="btn-secondary"
              >
                Cancel
              </button>
              <button type="submit" disabled={editLoading} className="btn-primary">
                {editLoading ? 'Saving...' : 'Save Changes'}
              </button>
            </div>
          </Form>
        </Modal>

        {/* Change Password Modal */}
        <Modal
          title="Change Password"
          open={passwordModalVisible}
          onCancel={() => setPasswordModalVisible(false)}
          footer={null}
          width={500}
        >
          <Form
            form={passwordForm}
            layout="vertical"
            onFinish={handleChangePassword}
            className="mt-6"
          >
            <Form.Item
              name="currentPassword"
              label={<span className="text-sm font-semibold text-stone-900">Current Password</span>}
              rules={[{ required: true, message: 'Please enter your current password' }]}
              className="mb-4"
            >
              <Input.Password placeholder="Enter your current password" className="input-field" size="large" />
            </Form.Item>

            <Form.Item
              name="newPassword"
              label={<span className="text-sm font-semibold text-stone-900">New Password</span>}
              rules={[
                { required: true, message: 'Please enter your new password' },
                { min: 8, message: 'Password must be at least 8 characters' },
              ]}
              className="mb-4"
            >
              <Input.Password placeholder="Enter your new password" className="input-field" size="large" />
            </Form.Item>

            <Form.Item
              name="confirmPassword"
              label={<span className="text-sm font-semibold text-stone-900">Confirm New Password</span>}
              dependencies={['newPassword']}
              rules={[
                { required: true, message: 'Please confirm your new password' },
                ({ getFieldValue }) => ({
                  validator(_, value) {
                    if (!value || getFieldValue('newPassword') === value) {
                      return Promise.resolve();
                    }
                    return Promise.reject(new Error('Passwords do not match'));
                  },
                }),
              ]}
              className="mb-6"
            >
              <Input.Password placeholder="Confirm your new password" className="input-field" size="large" />
            </Form.Item>

            <div className="flex gap-3 justify-end mt-8">
              <button
                type="button"
                onClick={() => setPasswordModalVisible(false)}
                className="btn-secondary"
              >
                Cancel
              </button>
              <button type="submit" disabled={passwordLoading} className="btn-primary">
                {passwordLoading ? 'Changing...' : 'Change Password'}
              </button>
            </div>
          </Form>
        </Modal>
      </div>
    </div>
  );
};

export default Profile;
