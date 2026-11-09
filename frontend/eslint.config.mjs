import js from '@eslint/js'
import pluginVue from 'eslint-plugin-vue'
import { withVueTs, vueTsConfigs } from '@vue/eslint-config-typescript'
import eslintConfigPrettier from 'eslint-config-prettier'

export default withVueTs(
  {
    ignores: ['**/dist/**', '**/coverage/**', '**/node_modules/**', '**/*.d.ts'],
  },

  js.configs.recommended,
  pluginVue.configs['flat/recommended'],
  vueTsConfigs.recommended,

  {
    rules: {
      // General
      'no-console': 'warn',
      'no-debugger': 'error',
      eqeqeq: ['error', 'always'],

      // TypeScript
      '@typescript-eslint/no-unused-vars': [
        'error',
        {
          argsIgnorePattern: '^_',
          varsIgnorePattern: '^_',
        },
      ],
      '@typescript-eslint/no-explicit-any': 'warn',

      // Vue
      'vue/multi-word-component-names': 'off',
      'vue/html-self-closing': [
        'error',
        {
          html: {
            void: 'always',
            normal: 'always',
            component: 'always',
          },
        },
      ],
    },
  },

  eslintConfigPrettier,
)
