import React, { useState } from 'react';
import { Sweet } from '../../types';
import '../Auth/Auth.css';

interface PurchaseModalProps {
  sweet: Sweet;
  onClose: () => void;
  onConfirm: (quantity: number) => void;
}

const PurchaseModal: React.FC<PurchaseModalProps> = ({ sweet, onClose, onConfirm }) => {
  const [quantity, setQuantity] = useState(1);
  const [error, setError] = useState('');

  const price = parseFloat(sweet.price);
  const totalPrice = price * quantity;
  const maxQuantity = sweet.quantity;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (quantity < 1) {
      setError('Quantity must be at least 1');
      return;
    }

    if (quantity > maxQuantity) {
      setError(`Only ${maxQuantity} items available in stock`);
      return;
    }

    onConfirm(quantity);
  };

  return (
    <div className="modal" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()} style={{ maxWidth: '500px' }}>
        <div className="modal-header">
          <h2>Purchase Confirmation</h2>
          <button className="close-btn" onClick={onClose}>&times;</button>
        </div>

        <div style={{ marginBottom: '24px' }}>
          <div style={{ 
            background: '#f8f9fa', 
            padding: '16px', 
            borderRadius: '8px',
            marginBottom: '20px'
          }}>
            <h3 style={{ margin: '0 0 16px 0', color: '#333' }}>{sweet.name}</h3>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span style={{ color: '#666', fontWeight: '500' }}>Category:</span>
                <span style={{ color: '#333' }}>{sweet.category}</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span style={{ color: '#666', fontWeight: '500' }}>Price per unit:</span>
                <span style={{ color: '#333', fontWeight: '600' }}>${price.toFixed(2)}</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span style={{ color: '#666', fontWeight: '500' }}>Available Stock:</span>
                <span style={{ color: '#333', fontWeight: '600' }}>{maxQuantity} units</span>
              </div>
            </div>
          </div>

          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label htmlFor="quantity" style={{ fontWeight: '600', marginBottom: '8px', display: 'block' }}>
                Quantity
              </label>
              <input
                type="number"
                id="quantity"
                min="1"
                max={maxQuantity}
                value={quantity}
                onChange={(e) => {
                  const val = parseInt(e.target.value) || 1;
                  setQuantity(Math.max(1, Math.min(val, maxQuantity)));
                  setError('');
                }}
                style={{
                  width: '100%',
                  padding: '12px',
                  border: '2px solid #e0e0e0',
                  borderRadius: '8px',
                  fontSize: '16px'
                }}
                required
              />
              <small style={{ color: '#666', fontSize: '0.85em', display: 'block', marginTop: '4px' }}>
                Maximum: {maxQuantity} units
              </small>
            </div>

            {error && <div className="error" style={{ marginBottom: '16px' }}>{error}</div>}

            <div style={{
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              padding: '16px',
              borderRadius: '8px',
              marginBottom: '20px',
              color: 'white'
            }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span style={{ fontSize: '18px', fontWeight: '600' }}>Total Price:</span>
                <span style={{ fontSize: '24px', fontWeight: '700' }}>${totalPrice.toFixed(2)}</span>
              </div>
              <div style={{ fontSize: '14px', opacity: 0.9, marginTop: '4px' }}>
                {quantity} {quantity === 1 ? 'unit' : 'units'} × ${price.toFixed(2)}
              </div>
            </div>

            <div style={{ display: 'flex', gap: '12px' }}>
              <button
                type="button"
                className="btn"
                onClick={onClose}
                style={{
                  flex: 1,
                  background: '#6c757d',
                  color: 'white',
                  padding: '12px 24px'
                }}
              >
                Cancel
              </button>
              <button
                type="submit"
                className="btn btn-success"
                style={{
                  flex: 1,
                  padding: '12px 24px'
                }}
              >
                Confirm Purchase
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default PurchaseModal;

