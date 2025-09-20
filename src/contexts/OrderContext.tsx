import React, { createContext, useContext, useReducer, ReactNode } from 'react';

export interface Package {
  id: string;
  name: string;
  price: number;
  originalPrice?: number;
  duration: string;
  features: string[];
  popular?: boolean;
  buttonText: string;
}

export interface OrderData {
  customer_email: string;
  package_id: string;
  full_name: string;
  phone_number: string;
}

interface OrderState {
  selectedPackage: Package | null;
  orderData: Partial<OrderData>;
  currentOrder: {
    order_id: string;
    checkout_url: string;
    reference: string;
    status: string;
  } | null;
  isLoading: boolean;
  error: string | null;
}

type OrderAction = 
  | { type: 'SET_SELECTED_PACKAGE'; payload: Package }
  | { type: 'UPDATE_ORDER_DATA'; payload: Partial<OrderData> }
  | { type: 'SET_CURRENT_ORDER'; payload: OrderState['currentOrder'] }
  | { type: 'SET_LOADING'; payload: boolean }
  | { type: 'SET_ERROR'; payload: string | null }
  | { type: 'RESET_ORDER' };

const initialState: OrderState = {
  selectedPackage: null,
  orderData: {},
  currentOrder: null,
  isLoading: false,
  error: null
};

const orderReducer = (state: OrderState, action: OrderAction): OrderState => {
  switch (action.type) {
    case 'SET_SELECTED_PACKAGE':
      return { ...state, selectedPackage: action.payload };
    case 'UPDATE_ORDER_DATA':
      return { ...state, orderData: { ...state.orderData, ...action.payload } };
    case 'SET_CURRENT_ORDER':
      return { ...state, currentOrder: action.payload };
    case 'SET_LOADING':
      return { ...state, isLoading: action.payload };
    case 'SET_ERROR':
      return { ...state, error: action.payload };
    case 'RESET_ORDER':
      return initialState;
    default:
      return state;
  }
};

const OrderContext = createContext<{
  state: OrderState;
  dispatch: React.Dispatch<OrderAction>;
} | null>(null);

export const OrderProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [state, dispatch] = useReducer(orderReducer, initialState);

  return (
    <OrderContext.Provider value={{ state, dispatch }}>
      {children}
    </OrderContext.Provider>
  );
};

export const useOrder = () => {
  const context = useContext(OrderContext);
  if (!context) {
    throw new Error('useOrder must be used within an OrderProvider');
  }
  return context;
};
