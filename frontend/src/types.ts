export interface Sweet {
  id: number;
  name: string;
  category: string;
  price: string;
  quantity: number;
  created_at: string;
  updated_at: string;
}

export interface User {
  id: number;
  username: string;
  email: string;
  role: string;
}

export interface PurchaseHistory {
  id: number;
  sweet_name: string;
  category: string;
  price: string;
  quantity: number;
  total_price: string;
  purchased_at: string;
}

export interface AdminPurchaseHistory {
  id: number;
  user_id: number;
  username: string;
  sweet_name: string;
  category: string;
  price: string;
  quantity: number;
  total_price: string;
  purchased_at: string;
}


