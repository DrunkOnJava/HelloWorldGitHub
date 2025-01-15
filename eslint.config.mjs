/** @type {import('eslint').Linter.Config} */
export default {
  files: ["**/*.{js,ts,jsx,tsx,astro}"],
  extends: ["eslint:recommended", "plugin:@typescript-eslint/recommended"],
  parser: "@typescript-eslint/parser",
  plugins: ["@typescript-eslint"],
  root: true,
  env: {
    node: true,
    browser: true,
    es2022: true,
  },
  parserOptions: {
    ecmaVersion: "latest",
    sourceType: "module",
    tsconfigRootDir: __dirname,
    project: ["./tsconfig.json"],
  },
  settings: {
    "import/resolver": {
      typescript: {},
    },
  },
  rules: {
    "no-unused-vars": "off",
    "@typescript-eslint/no-unused-vars": ["warn"],
    "@typescript-eslint/consistent-type-imports": "warn",
    "@typescript-eslint/no-explicit-any": "warn",
    "@typescript-eslint/explicit-function-return-type": "off",
    "@typescript-eslint/explicit-module-boundary-types": "off",
  },
  ignorePatterns: ["node_modules", "dist", ".astro"],
};
