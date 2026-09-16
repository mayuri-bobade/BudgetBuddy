import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

export default function Register() {
  const [formData, setFormData] = useState({
    username: '', email: '', password: '', password_confirm: '', first_name: '', last_name: '',
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { register } = useAuth();
  const navigate = useNavigate();

  const handleChange = (e) => setFormData({ ...formData, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    if (formData.password !== formData.password_confirm) { setError('Passwords do not match'); return; }
    setLoading(true);
    try {
      await register(formData);
      navigate('/dashboard');
    } catch (err) {
      const detail = err.response?.data?.detail;
      if (typeof detail === 'string') setError(detail);
      else if (Array.isArray(detail)) setError(detail.map((d) => d.msg || d).join(', '));
      else if (typeof detail === 'object') setError(JSON.stringify(detail));
      else setError('Registration failed. Please try again.');
    } finally { setLoading(false); }
  };

  return (
    <div className="auth-container">
      <div className="auth-card auth-card-wide">
        <div className="auth-brand">
          <div className="auth-brand-mark">B</div>
          <span className="auth-brand-name">BudgetBuddy</span>
        </div>

        <h2>Create your account</h2>
        <p className="auth-subtitle">Start managing your finances</p>

        {error && <div className="error-message">{error}</div>}

        <form onSubmit={handleSubmit}>
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="first_name">First name</label>
              <input type="text" id="first_name" name="first_name" value={formData.first_name} onChange={handleChange} placeholder="John" autoComplete="given-name" />
            </div>
            <div className="form-group">
              <label htmlFor="last_name">Last name</label>
              <input type="text" id="last_name" name="last_name" value={formData.last_name} onChange={handleChange} placeholder="Doe" autoComplete="family-name" />
            </div>
          </div>
          <div className="form-group">
            <label htmlFor="username">Username *</label>
            <input type="text" id="username" name="username" value={formData.username} onChange={handleChange} required placeholder="johndoe" autoComplete="username" />
          </div>
          <div className="form-group">
            <label htmlFor="email">Email *</label>
            <input type="email" id="email" name="email" value={formData.email} onChange={handleChange} required placeholder="john@example.com" autoComplete="email" />
          </div>
          <div className="form-group">
            <label htmlFor="password">Password *</label>
            <input type="password" id="password" name="password" value={formData.password} onChange={handleChange} required minLength={8} placeholder="Min 8 characters" autoComplete="new-password" />
          </div>
          <div className="form-group">
            <label htmlFor="password_confirm">Confirm password *</label>
            <input type="password" id="password_confirm" name="password_confirm" value={formData.password_confirm} onChange={handleChange} required minLength={8} placeholder="Repeat password" autoComplete="new-password" />
          </div>
          <button type="submit" className="btn-primary" disabled={loading}>
            {loading ? 'Creating account...' : 'Create account'}
          </button>
        </form>

        <p className="auth-link">
          Already have an account? <Link to="/login">Sign in</Link>
        </p>
      </div>
    </div>
  );
}
