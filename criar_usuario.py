from supabase_client import supabase

try:
    print("Tentando criar o usuário admin@admin.com...")
    # O Supabase pode exigir confirmação de email, vamos tentar criar direto
    response = supabase.auth.sign_up({
        "email": "admin@admin.com",
        "password": "admin123"
    })
    if response.user:
        print("\n[OK] USUÁRIO CRIADO COM SUCESSO!")
        print("Email: admin@admin.com")
        print("Senha: admin123")
    else:
        print("\n[AVISO] O usuário pode já existir.")
except Exception as e:
    print(f"\n[ERRO] {e}")
    print("\nDICA: Se o erro for 'Email not confirmed', vá no site do Supabase > Authentication > Providers > Email e desmarque a opção 'Confirm email'.")
