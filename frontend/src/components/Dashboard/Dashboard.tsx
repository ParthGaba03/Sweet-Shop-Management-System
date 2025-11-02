import React, { useState, useEffect } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import axios from 'axios';
import SweetCard from './SweetCard';
import SweetModal from './SweetModal';
import PurchaseModal from './PurchaseModal';
import { Sweet, PurchaseHistory, AdminPurchaseHistory } from '../../types';
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
  const [allCategories, setAllCategories] = useState<string[]>([]); // Store all categories separately
  const [showPurchaseModal, setShowPurchaseModal] = useState(false);
  const [purchasingSweet, setPurchasingSweet] = useState<Sweet | null>(null);
  const [purchaseHistory, setPurchaseHistory] = useState<PurchaseHistory[]>([]);
  const [adminPurchaseHistory, setAdminPurchaseHistory] = useState<AdminPurchaseHistory[]>([]);
  const [showHistory, setShowHistory] = useState(false);

  useEffect(() => {
    fetchSweets();
    fetchAllCategories();
    if (isAdmin()) {
      fetchAdminPurchaseHistory();
    } else {
      fetchPurchaseHistory();
    }
  }, []);

  const fetchAllCategories = async () => {
    try {
      // Fetch all sweets to get all categories (without filters)
      const response = await axios.get(getApiUrl('/api/sweets/'));
      const allSweets = response.data as Sweet[];
      const categories = Array.from(new Set(allSweets.map(s => s.category)));
      setAllCategories(categories);
    } catch (err) {
      console.error('Error fetching categories:', err);
    }
  };

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

  const handlePurchaseClick = (sweet: Sweet) => {
    // Only allow purchase for non-admin users
    if (!isAdmin()) {
      setPurchasingSweet(sweet);
      setShowPurchaseModal(true);
    }
  };

  const fetchPurchaseHistory = async () => {
    try {
      const response = await axios.get(getApiUrl('/api/sweets/purchase-history'));
      setPurchaseHistory(response.data);
    } catch (err) {
      console.error('Error fetching purchase history:', err);
    }
  };

  const fetchAdminPurchaseHistory = async () => {
    try {
      const response = await axios.get(getApiUrl('/api/sweets/admin/purchase-history'));
      setAdminPurchaseHistory(response.data);
    } catch (err) {
      console.error('Error fetching admin purchase history:', err);
    }
  };

  const handlePurchase = async (sweet: Sweet, quantity: number) => {
    try {
      await axios.post(getApiUrl(`/api/sweets/${sweet.id}/purchase`), { quantity });
      fetchSweets();
      fetchPurchaseHistory(); // Refresh purchase history after purchase
      setShowPurchaseModal(false);
      setPurchasingSweet(null);
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
      const errorMsg = err.response?.data?.detail || 'Delete failed';
      alert(errorMsg);
      console.error('Delete error:', err);
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
            {allCategories.map(cat => (
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

        <div style={{ display: 'flex', gap: '12px', marginBottom: '20px', flexWrap: 'wrap' }}>
        {isAdmin() && (
            <>
              <div className="admin-actions" style={{ borderTop: 'none', paddingTop: 0, margin: 0 }}>
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
              <button
                className="btn"
                onClick={() => {
                  setShowHistory(!showHistory);
                  if (!showHistory) {
                    fetchAdminPurchaseHistory();
                  }
                }}
                style={{
                  background: showHistory ? '#6c757d' : 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                  color: 'white',
                  padding: '12px 24px'
                }}
              >
                {showHistory ? 'Hide All Purchases' : 'View All Purchases'}
              </button>
            </>
          )}
          
          {!isAdmin() && (
            <button
              className="btn"
              onClick={() => {
                setShowHistory(!showHistory);
                if (!showHistory) {
                  fetchPurchaseHistory();
                }
              }}
              style={{
                background: showHistory ? '#6c757d' : 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                color: 'white',
                padding: '12px 24px'
              }}
            >
              {showHistory ? 'Hide Purchase History' : 'View Purchase History'}
            </button>
          )}
        </div>

        {showHistory && (
          <div className="card" style={{ marginBottom: '24px' }}>
            <h2 style={{ marginBottom: '20px', color: '#333' }}>
              {isAdmin() ? '📊 My Sweets Purchase History' : '📦 Your Purchase History'}
            </h2>
            {(isAdmin() ? adminPurchaseHistory : purchaseHistory).length === 0 ? (
              <p style={{ color: '#666', textAlign: 'center', padding: '20px' }}>
                {isAdmin() 
                  ? 'No purchases found for your sweets yet. Users will see their purchases here once they start shopping your sweets.'
                  : 'No purchases yet. Start shopping to see your history here!'}
              </p>
            ) : (
              <div style={{ overflowX: 'auto' }}>
                <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                  <thead>
                    <tr style={{ background: '#f8f9fa', borderBottom: '2px solid #dee2e6' }}>
                      {isAdmin() && (
                        <th style={{ padding: '12px', textAlign: 'left', fontWeight: '600', color: '#495057' }}>User</th>
                      )}
                      <th style={{ padding: '12px', textAlign: 'left', fontWeight: '600', color: '#495057' }}>Date</th>
                      <th style={{ padding: '12px', textAlign: 'left', fontWeight: '600', color: '#495057' }}>Sweet Name</th>
                      <th style={{ padding: '12px', textAlign: 'left', fontWeight: '600', color: '#495057' }}>Category</th>
                      <th style={{ padding: '12px', textAlign: 'right', fontWeight: '600', color: '#495057' }}>Quantity</th>
                      <th style={{ padding: '12px', textAlign: 'right', fontWeight: '600', color: '#495057' }}>Unit Price</th>
                      <th style={{ padding: '12px', textAlign: 'right', fontWeight: '600', color: '#495057' }}>Total Price</th>
                    </tr>
                  </thead>
                  <tbody>
                    {(isAdmin() ? adminPurchaseHistory : purchaseHistory).map((purchase) => (
                      <tr key={purchase.id} style={{ borderBottom: '1px solid #dee2e6' }}>
                        {isAdmin() && 'username' in purchase && (
                          <td style={{ padding: '12px', fontWeight: '500', color: '#667eea' }}>
                            {(purchase as AdminPurchaseHistory).username}
                          </td>
                        )}
                        <td style={{ padding: '12px', color: '#666' }}>
                          {new Date(purchase.purchased_at).toLocaleString()}
                        </td>
                        <td style={{ padding: '12px', fontWeight: '500', color: '#333' }}>
                          {purchase.sweet_name}
                        </td>
                        <td style={{ padding: '12px', color: '#666' }}>{purchase.category}</td>
                        <td style={{ padding: '12px', textAlign: 'right', color: '#333' }}>
                          {purchase.quantity}
                        </td>
                        <td style={{ padding: '12px', textAlign: 'right', color: '#666' }}>
                          ₹{parseFloat(purchase.price).toFixed(2)}
                        </td>
                        <td style={{ padding: '12px', textAlign: 'right', fontWeight: '600', color: '#667eea' }}>
                          ₹{parseFloat(purchase.total_price).toFixed(2)}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                  {!isAdmin() && (
                    <tfoot>
                      <tr style={{ background: '#f8f9fa', borderTop: '2px solid #dee2e6' }}>
                        <td colSpan={isAdmin() ? 6 : 5} style={{ padding: '12px', textAlign: 'right', fontWeight: '600', color: '#495057' }}>
                          Total Spent:
                        </td>
                        <td style={{ padding: '12px', textAlign: 'right', fontWeight: '700', color: '#667eea', fontSize: '18px' }}>
                          ₹{purchaseHistory.reduce((sum, p) => sum + parseFloat(p.total_price), 0).toFixed(2)}
                        </td>
                      </tr>
                    </tfoot>
                  )}
                  {isAdmin() && (
                    <tfoot>
                      <tr style={{ background: '#f8f9fa', borderTop: '2px solid #dee2e6' }}>
                        <td colSpan={6} style={{ padding: '12px', textAlign: 'right', fontWeight: '600', color: '#495057' }}>
                          Total Revenue:
                        </td>
                        <td style={{ padding: '12px', textAlign: 'right', fontWeight: '700', color: '#667eea', fontSize: '18px' }}>
                          ₹{adminPurchaseHistory.reduce((sum, p) => sum + parseFloat(p.total_price), 0).toFixed(2)}
                        </td>
                      </tr>
                    </tfoot>
                  )}
                </table>
              </div>
            )}
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
                onPurchase={handlePurchaseClick}
                onRestock={isAdmin() && sweet.created_by_user_id === user?.id ? handleRestock : undefined}
                onEdit={isAdmin() && sweet.created_by_user_id === user?.id ? handleEdit : undefined}
                onDelete={isAdmin() && sweet.created_by_user_id === user?.id ? handleDelete : undefined}
                isAdmin={isAdmin()}
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

        {showPurchaseModal && purchasingSweet && (
          <PurchaseModal
            sweet={purchasingSweet}
            onClose={() => {
              setShowPurchaseModal(false);
              setPurchasingSweet(null);
            }}
            onConfirm={(quantity) => handlePurchase(purchasingSweet, quantity)}
          />
        )}
      </div>
    </div>
  );
};

export default Dashboard;

