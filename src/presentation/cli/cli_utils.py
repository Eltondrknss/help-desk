def non_empty_input(prompt: str) -> str:
    
    while True:
        user_input = input(prompt).strip()
        if user_input:
            return user_input
        print("❌ Este campo não pode ser vazio.")