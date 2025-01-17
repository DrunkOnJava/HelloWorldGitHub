# Project Name

A React TypeScript project created with the project scaffolding tool.

## Getting Started

1. Install dependencies:
   ```bash
   npm install
   ```

2. Start the development server:
   ```bash
   npm run dev
   ```

3. Open [http://localhost:3000](http://localhost:3000) to view the app in your browser.

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run test` - Run tests
- `npm run lint` - Run ESLint
- `npm run format` - Format code with Prettier

## Project Structure

```
src/
  ├── components/     # Reusable UI components
  ├── pages/         # Page components
  ├── hooks/         # Custom React hooks
  ├── utils/         # Utility functions
  ├── types/         # TypeScript type definitions
  ├── assets/        # Static assets
  │   ├── images/    # Image files
  │   └── styles/    # Global styles
  └── __tests__/     # Test files
      ├── components/
      ├── pages/
      └── hooks/
```

## Adding New Components

Use the scaffolding tool to create new components:

```bash
npm run scaffold component MyComponent
```

## Adding New Pages

Use the scaffolding tool to create new pages:

```bash
npm run scaffold page MyPage
```

## Testing

Tests are written using Jest and React Testing Library. Run tests with:

```bash
npm test
```

## Contributing

1. Create a feature branch
2. Commit your changes
3. Push to the branch
4. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
