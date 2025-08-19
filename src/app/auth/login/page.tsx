// src/app/auth/login/page.tsx
import { LoginForm } from '@/components/features/auth/LoginForm';

export default function LoginPage() {
  return (
    <div className="min-h-[60vh] flex items-center justify-center">
      <LoginForm />
    </div>
  );
}