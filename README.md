# Password Generator CLI

This password generator has been designed based on NIST, NCSC, and OWASP recommendations, such as:

- [NIST 800-63](https://csrc.nist.gov/publications/detail/sp/800-63-3/final)
- [OWASP ASVS 4.0](https://owasp.org/www-project-application-security-verification-standard/)
- [OWASP Password Policy Standards](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [NIST SP800-63B](https://csrc.nist.gov/publications/detail/sp/800-63b/final)

## 1. Clone the Repository

To get started, clone the repository:

```bash
git clone https://github.com/pravallika-nunna/Password-Generator-CLI
```

## Workflow

### 1. Execution Flow 
- The execution starts from the main method:
```
  generator = PasswordGenerator()
  generator.generate_password()
```
- This initializes the PasswordGenerator class and calls the generate_password() method.
  
### 2. generate_password() Method
- Takes user input for password preferences.
- Validates each input.
- Instantiates the Password class:

```
  password_instance = Password(self.options)
```

- A loop continues to generate passwords until the user decides to stop:

```
while True:
    try:
        if self.keyword:
            print("Generated Password:", password_instance.password_generator(keyword=self.keyword))
        else:
            print("Generated Password:", password_instance.password_generator())
    except ValueError as e:
        print(e)

    another = input("Do you want to generate another password with the same input? (y/n): ").strip().lower()
    if another != 'y':
        print("Thank you for using the password generator!")
        break
```

### 3. password_generator() Method
- Generates a password based on user preferences:
  - Static random generation: Generates random characters based on user-selected options.
  - Keyword addition (optional): If a keyword is provided, it is inserted randomly into the password.
  - Shuffling: The static and random parts of the password are shuffled to ensure randomness.
  - Return: The final password is returned.


## Password principles followed

### 1. No silent truncation
- If the provided keyword length and selected options don't allow for a valid password to be generated, the user will be informed instead of silently truncating the keyword.
 
### 2. Password Length
- The length of the password is more important than its complexity. Industry standards recommend a password length between 12-62 characters.

### 3. Optional complexity
- The generator allows flexibility in complexity. The user isn't forced to select any specific options, ensuring that length remains the primary factor for password strength.
- Following OWASP ASVS 4.0 (March 2019) recommendations: "Verify that there are no password composition rules limiting the type of characters permitted" (C6).

### 4. Allwoing all UTF characters
- The generator supports all characters, including special characters, ensuring compatibility with UTF-8.

### 5.  Flexibility and Customization
- Users can specify different options for password complexity, but the generator focuses on length as the most important aspect, in line with best practices.

### 6. Exclude characters
- If you have beef with some words or chars, you can surely exclude them from the password.


```

I have organized the sections with proper headings and explanations. This should help users understand how to use the password generator, the workflow, and the principles followed in its design.

```