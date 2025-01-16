import random
import string
from typing import Dict, Any, Optional

class Password:
    def __init__(self, options: Dict[str, Any]) -> None:
        self.include_upper = options.get('include_upper', False)
        self.include_lower = options.get('include_lower', False)
        self.include_numbers = options.get('include_numbers', False)
        self.include_special = options.get('include_special', False)
        self.exclude_char = options.get('exclude_char', '')
        self.length = options.get('length', 12)

        # Define character sets
        self.lowercase = ''.join(c for c in string.ascii_lowercase if c not in self.exclude_char) if self.include_lower else ""
        self.uppercase = ''.join(c for c in string.ascii_uppercase if c not in self.exclude_char) if self.include_upper else ""
        self.digits = ''.join(c for c in string.digits if c not in self.exclude_char) if self.include_numbers else ""
        self.special = ''.join(c for c in "-_.@#$?" if c not in self.exclude_char) if self.include_special else ""

        # All character sets combined
        self.all_characters = self.lowercase + self.uppercase + self.digits + self.special

    def static_random_segment(self) -> str:
        """
        Generate a static random segment containing at least one character
        from each enabled character set (lowercase, uppercase, digits, special).
        """
        segment = ""
        if self.include_lower and self.lowercase:
            segment += random.choice(self.lowercase)
        if self.include_upper and self.uppercase:
            segment += random.choice(self.uppercase)
        if self.include_numbers and self.digits:
            segment += random.choice(self.digits)
        if self.include_special and self.special:
            segment += random.choice(self.special)

        return segment

    def random_segment(self, segment_length: int) -> str:
        """
        Generate a random segment using any printable UTF characters,
        excluding explicitly excluded characters.
        """
        utf_chars = ''.join(c for c in string.printable if c not in self.exclude_char)
        return ''.join(random.choice(utf_chars) for _ in range(segment_length))

    def password_generator(self, keyword: str = "") -> str:
        """
        Generate a password with the given options. If a keyword is provided,
        it will be added as a single word at a random position.
        """
        # Ensure the password meets complexity requirements
        static_part = self.static_random_segment()

        # Remaining length after adding the static part and keyword
        remaining_length = self.length - len(static_part) - len(keyword)
        if remaining_length < 0:
            raise ValueError("Keyword and static part length exceed the specified password length.")

        # Generate the random segments
        random_part = self.random_segment(remaining_length)

        # Combine all parts and shuffle
        password_parts = list(static_part + random_part)
        random.shuffle(password_parts)

        # Convert to string
        password = ''.join(password_parts)

        # Insert keyword at a random position, if provided
        if keyword:
            insert_position = random.randint(0, len(password))
            password = password[:insert_position] + keyword + password[insert_position:]

        return password

class PasswordGenerator:
    def __init__(self) -> None:
        self.options: Dict[str, Any] = {
            'include_upper': False,
            'include_lower': False,
            'include_numbers': False,
            'include_special': False,
            'exclude_char': '',
            'length': 12
        }
        self.keyword: Optional[str] = None

    def validate_input_length(self) -> bool:
        """
        Validate if the user-provided length meets the necessary criteria.
        """
        required_min_length = len(self.keyword) + sum(
            1 for key in ['include_upper', 'include_lower', 'include_numbers', 'include_special'] if self.options[key]
        )

        if self.options['length'] < required_min_length:
            print(f"Password length must be at least {required_min_length} characters to meet the requirements.")
            return False

        return True

    def get_user_input(self) -> None:
        """
        Collect user input for password options.
        """
        self.keyword = input("Enter a keyword (Optional): ").strip()

        def validate_yes_no(prompt: str) -> bool:
            while True:
                value = input(prompt).strip().lower()
                if value in ['y', 'n']:
                    return value == 'y'
                print("Invalid input. Please enter 'y' or 'n'.")

        def validate_positive_int(prompt: str) -> int:
            while True:
                try:
                    value = int(input(prompt))
                    if 12 <= value <= 64:
                        return value
                    print("Password length must be between 12 and 64 characters.")
                except ValueError:
                    print("Invalid input. Please enter a valid positive integer.")

        self.options['include_upper'] = validate_yes_no("Include uppercase letters? (y/n): ")
        self.options['include_lower'] = validate_yes_no("Include lowercase letters? (y/n): ")
        self.options['include_numbers'] = validate_yes_no("Include numbers? (y/n): ")
        self.options['include_special'] = validate_yes_no("Include special characters? (y/n): ")
        self.options['exclude_char'] = input("Any characters to exclude? ").strip()
        self.options['length'] = validate_positive_int("Enter the desired password length: ")

        # Validate the length
        while not self.validate_input_length():
            self.options['length'] = validate_positive_int("Enter a valid password length: ")

    def generate_password(self) -> None:
        """
        Generate and display the password based on user input.
        """
        self.get_user_input()

        # Instantiate the Password class
        password_instance = Password(self.options)

        while True:
            # Generate the password
            try:
                if self.keyword:
                    print("Generated Password:", password_instance.password_generator(keyword=self.keyword))
                else:
                    print("Generated Password:", password_instance.password_generator())
            except ValueError as e:
                print(e)

            # Ask if the user wants to generate another password
            another = input("Do you want to generate another password with the same input? (y/n): ").strip().lower()
            if another != 'y':
                print("Thank you for using the password generator!")
                break

if __name__ == "__main__":
    generator = PasswordGenerator()
    generator.generate_password()