import React, { useState, useEffect } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import axios from 'axios';
import SweetCard from './SweetCard';
import SweetModal from './SweetModal';
import { Sweet } from '../../types';
import { getApiUrl } from '../../config';
import '../Dashboard/Dashboard.css';

const Dashboard: React.FC = () => {
  const { user, logout, isAdmin } = useAuth();
  const [sweets, setSweets] = useState<Sweet[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [searchTerm, setSearchTerm] = useState('');
  const [categoryFilter, setCategoryFilter] = useState('');
  const [minPrice, setMinPrice] = useState('');
  const [maxPrice, setMaxPrice] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [editingSweet, setEditingSweet] = useState<Sweet | null>(null);

  useEffect(() => {
    fetchSweets();
  }, []);

  const fetchSweets = async () => {
    try {
      setLoading(true);
      const params = new URLSearchParams();
      if (searchTerm) params.append('name', searchTerm);
      if (categoryFilter) params.append('category', categoryFilter);
      if (minPrice) params.append('min_price', minPrice);
      if (maxPrice) params.append('max_price', maxPrice);

      const url = params.toString() 
        ? `/api/sweets/search?${params.toString()}` 
        : '/api/sweets/';
      
      const response = await axios.get(getApiUrl(url));
      setSweets(response.data);
      setError('');
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || err.message || 'Failed to load sweets. Please try again.';
      setError(errorMessage);
      console.error('Error fetching sweets:', err);
      console.error('Response:', err.response);
      if (err.response?.status === 401) {
        setError('Authentication failed. Please login again.');
      } else if (err.response?.status === 403) {
        setError('Access denied. You do not have permission.');
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const debounce = setTimeout(() => {
      fetchSweets();
    }, 300);
    return () => clearTimeout(debounce);
  }, [searchTerm, categoryFilter, minPrice, maxPrice]);

  const handlePurchase = async (id: number, quantity: number = 1) => {
    try {
      await axios.post(getApiUrl(`/api/sweets/${id}/purchase`), { quantity });
      fetchSweets();
    } catch (err: any) {
      alert(err.response?.data?.detail || 'Purchase failed');
    }
  };

  const handleRestock = async (id: number, quantity: number) => {
    try {
      await axios.post(getApiUrl(`/api/sweets/${id}/restock`), { quantity });
      fetchSweets();
      setShowModal(false);
    } catch (err: any) {
      alert(err.response?.data?.detail || 'Restock failed');
    }
  };

  const handleDelete = async (id: number) => {
    if (!window.confirm('Are you sure you want to delete this sweet?')) return;
    
    try {
      await axios.delete(getApiUrl(`/api/sweets/${id}/`));
      fetchSweets();
    } catch (err: any) {
      alert(err.response?.data?.detail || 'Delete failed');
    }
  };

  const handleEdit = (sweet: Sweet) => {
    setEditingSweet(sweet);
    setShowModal(true);
  };

  const handleSave = async (sweetData: any) => {
    console.log('🚀 handleSave called with:', sweetData);
    console.log('🔑 Authorization header:', axios.defaults.headers.common['Authorization']);
    
    try {
      if (editingSweet) {
        console.log('📝 Editing sweet:', editingSweet.id);
        await axios.put(getApiUrl(`/api/sweets/${editingSweet.id}/`), sweetData);
      } else {
        console.log('➕ Creating new sweet:', sweetData);
        console.log('📤 Request config:', {
          url: '/api/sweets',
          method: 'POST',
          headers: axios.defaults.headers.common,
          data: sweetData
        });
        const response = await axios.post(getApiUrl('/api/sweets/'), sweetData, {
          headers: {
            'Authorization': axios.defaults.headers.common['Authorization'],
            'Content-Type': 'application/json'
          }
        });
        console.log('✅ Success response:', response.data);
      }
      fetchSweets();
      setShowModal(false);
      setEditingSweet(null);
    } catch (err: any) {
      console.error('❌ Save error full:', err);
      console.error('❌ Error response:', err.response);
      console.error('❌ Error status:', err.response?.status);
      console.error('❌ Error data:', err.response?.data);
      console.error('❌ Error headers:', err.response?.headers);
      
      const errorMsg = err.response?.data?.detail || err.message || 'Save failed';
      if (err.response?.status === 403) {
        const detail = err.response?.data?.detail || '';
        alert(`Access denied (403). ${detail}\n\nPlease check:\n1. Browser console (F12) for details\n2. Backend terminal for logs\n3. Make sure you logged out and logged in again`);
      } else {
        alert(errorMsg);
      }
    }
  };

  const categories = Array.from(new Set(sweets.map(s => s.category)));

  return (
    <div>
      <div className="header">
        <div className="container">
          <h1>🍬 Sweet Shop Management System</h1>
          <div className="user-info">
            Welcome, {user?.username}! ({user?.role})
          </div>
          <button className="btn logout-btn" onClick={logout}>
            Logout
          </button>
        </div>
      </div>

      <div className="container">
        {error && <div className="error">{error}</div>}

        <div className="search-bar">
          <input
            type="text"
            placeholder="Search sweets by name..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>

        <div className="filters">
          <select
            value={categoryFilter}
            onChange={(e) => setCategoryFilter(e.target.value)}
          >
            <option value="">All Categories</option>
            {categories.map(cat => (
              <option key={cat} value={cat}>{cat}</option>
            ))}
          </select>
          <input
            type="number"
            placeholder="Min Price"
            value={minPrice}
            onChange={(e) => setMinPrice(e.target.value)}
            step="0.01"
            min="0"
          />
          <input
            type="number"
            placeholder="Max Price"
            value={maxPrice}
            onChange={(e) => setMaxPrice(e.target.value)}
            step="0.01"
            min="0"
          />
        </div>

        {isAdmin() && (
          <div className="admin-actions">
            <button
              className="btn btn-primary"
              onClick={() => {
                setEditingSweet(null);
                setShowModal(true);
              }}
            >
              + Add New Sweet
            </button>
          </div>
        )}

        {loading ? (
          <div>Loading sweets...</div>
        ) : sweets.length === 0 ? (
          <div className="card">No sweets found.</div>
        ) : (
          <div className="grid">
            {sweets.map(sweet => (
              <SweetCard
                key={sweet.id}
                sweet={sweet}
                onPurchase={handlePurchase}
                onRestock={isAdmin() ? handleRestock : undefined}
                onEdit={isAdmin() ? handleEdit : undefined}
                onDelete={isAdmin() ? handleDelete : undefined}
              />
            ))}
          </div>
        )}

        {showModal && (
          <SweetModal
            sweet={editingSweet}
            onClose={() => {
              setShowModal(false);
              setEditingSweet(null);
            }}
            onSave={handleSave}
          />
        )}
      </div>
    </div>
  );
};

export default Dashboard;

