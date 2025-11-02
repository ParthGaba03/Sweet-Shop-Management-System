import React, { useState } from 'react';
import { Sweet } from '../../types';
import './SweetCard.css';

interface SweetCardProps {
  sweet: Sweet;
  onPurchase: (id: number, quantity?: number) => void;
  onRestock?: (id: number, quantity: number) => void;
  onEdit?: (sweet: Sweet) => void;
  onDelete?: (id: number) => void;
}

const SweetCard: React.FC<SweetCardProps> = ({
  sweet,
  onPurchase,
  onRestock,
  onEdit,
  onDelete,
}) => {
  const [restockQuantity, setRestockQuantity] = useState('');

  const isOutOfStock = sweet.quantity === 0;

  return (
    <div className="sweet-card">
      <h3>{sweet.name}</h3>
      <div className="category">{sweet.category}</div>
      <div className="price">${parseFloat(sweet.price).toFixed(2)}</div>
      <div className={`quantity ${isOutOfStock ? 'out-of-stock' : ''}`}>
        {isOutOfStock ? 'Out of Stock' : `Stock: ${sweet.quantity}`}
      </div>

      <div className="card-actions">
        <button
          className="btn btn-success"
          onClick={() => onPurchase(sweet.id, 1)}
          disabled={isOutOfStock}
        >
          Purchase
        </button>

        {onRestock && (
          <div className="restock-section">
            <input
              type="number"
              min="1"
              value={restockQuantity}
              onChange={(e) => setRestockQuantity(e.target.value)}
              placeholder="Qty"
              style={{ width: '60px', marginRight: '8px', padding: '6px' }}
            />
            <button
              className="btn btn-primary"
              onClick={() => {
                const qty = parseInt(restockQuantity);
                if (qty > 0) {
                  onRestock(sweet.id, qty);
                  setRestockQuantity('');
                }
              }}
            >
              Restock
            </button>
          </div>
        )}

        {onEdit && (
          <button
            className="btn btn-primary"
            onClick={() => onEdit(sweet)}
            style={{ marginTop: '8px', width: '100%' }}
          >
            Edit
          </button>
        )}

        {onDelete && (
          <button
            className="btn btn-danger"
            onClick={() => onDelete(sweet.id)}
            style={{ marginTop: '8px', width: '100%' }}
          >
            Delete
          </button>
        )}
      </div>
    </div>
  );
};

export default SweetCard;

