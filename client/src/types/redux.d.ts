// redux.d.ts

import { Action, ThunkAction } from '@reduxjs/toolkit';
import { store } from '../store'; // Adjust the path according to your project structure

// ==============================
// 1. RootState Type
// ==============================

/**
 * Represents the entire Redux state tree.
 */
export type RootState = ReturnType<typeof store.getState>;

// ==============================
// 2. AppDispatch Type
// ==============================

/**
 * Represents the dispatch function from the Redux store.
 * Includes Thunk middleware for asynchronous actions.
 */
export type AppDispatch = typeof store.dispatch;

// ==============================
// 3. ThunkAction Type
// ==============================

/**
 * Represents a Thunk action.
 * @template R - The return type of the thunk.
 * @template E - The type of the extra argument injected into the thunk.
 */
export type AppThunk<ReturnType = void> = ThunkAction<
  ReturnType,
  RootState,
  unknown,
  Action<string>
>;

// ==============================
// 4. Typed Hooks
// ==============================

import { TypedUseSelectorHook, useDispatch, useSelector } from 'react-redux';

/**
 * A typed version of the `useDispatch` hook for the app.
 */
export const useAppDispatch: () => AppDispatch = useDispatch;

/**
 * A typed version of the `useSelector` hook for the app.
 */
export const useAppSelector: TypedUseSelectorHook<RootState> = useSelector;

// ==============================
// 5. Additional Types (Optional)
// ==============================

/**
 * Example User Interface
 */
export interface User {
  id: string;
  name: string;
  email: string;
  // Add other user-related fields
}

/**
 * Example Product Interface
 */
export interface Product {
  id: string;
  name: string;
  price: number;
  description: string;
  // Add other product-related fields
}

/**
 * Example Payment Interface
 */
export interface Payment {
  id: string;
  userId: string;
  amount: number;
  currency: string;
  status: 'pending' | 'completed' | 'failed';
  // Add other payment-related fields
}

// ==============================
// 6. Slice State Interfaces
// ==============================

/**
 * User Slice State
 */
export interface UserState {
  currentUser: User | null;
  loading: boolean;
  error: string | null;
}

/**
 * Products Slice State
 */
export interface ProductsState {
  products: Product[];
  loading: boolean;
  error: string | null;
}

/**
 * Payments Slice State
 */
export interface PaymentsState {
  payments: Payment[];
  loading: boolean;
  error: string | null;
}

// ==============================
// 7. Root Reducer Interface
// ==============================

/**
 * Represents the combined state of all Redux slices.
 */
export interface RootReducer {
  user: UserState;
  products: ProductsState;
  payments: PaymentsState;
  // Add other slices here
}
