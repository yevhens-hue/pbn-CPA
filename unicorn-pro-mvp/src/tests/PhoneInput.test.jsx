import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import PhoneInput from '../components/PhoneInput';

describe('PhoneInput Component', () => {
  it('should render an input field', () => {
    render(<PhoneInput value="" onChange={vi.fn()} />);
    const input = screen.getByRole('textbox');
    expect(input).toBeInTheDocument();
  });

  it('should format input as US phone number', () => {
    const handleChange = vi.fn();
    render(<PhoneInput value="" onChange={handleChange} />);
    const input = screen.getByRole('textbox');

    fireEvent.change(input, { target: { value: '1234567890' } });
    
    // The component should call onChange with the raw numeric value
    expect(handleChange).toHaveBeenCalledWith('1234567890');
    // For a real controlled component, the parent updates the value, 
    // but we can test if the component formats an incoming prop value correctly.
  });

  it('should display correctly formatted value when passed as prop', () => {
    render(<PhoneInput value="1234567890" onChange={vi.fn()} />);
    const input = screen.getByRole('textbox');
    expect(input.value).toBe('(123) 456-7890');
  });

  it('should show error if value length is > 0 and < 10', () => {
    render(<PhoneInput value="123" onChange={vi.fn()} error="Too short" />);
    const errorText = screen.getByText('Too short');
    expect(errorText).toBeInTheDocument();
    expect(errorText).toHaveStyle({ color: 'rgb(255, 0, 0)' });
  });
});
