// @ts-check
import { themes as prismThemes } from 'prism-react-renderer';

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Financial Agent Docs',
  tagline: 'Comprehensive system documentation for the Financial Agent application',
  favicon: 'img/favicon.ico',

  future: {
    v4: true,
  },

  url: 'http://localhost',
  baseUrl: '/',

  onBrokenLinks: 'warn',
  onBrokenMarkdownLinks: 'warn',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  markdown: {
    mermaid: true,
  },
  themes: ['@docusaurus/theme-mermaid'],

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: './sidebars.js',
          routeBasePath: '/',
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      colorMode: {
        defaultMode: 'dark',
        respectPrefersColorScheme: true,
      },
      navbar: {
        title: 'Financial Agent',
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'docsSidebar',
            position: 'left',
            label: '📖 Documentation',
          },
          {
            href: 'http://localhost:8000/docs',
            label: 'API Swagger',
            position: 'right',
          },
          {
            href: 'http://localhost:5174',
            label: 'Frontend',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Documentation',
            items: [
              { label: 'Architecture', to: '/architecture/overview' },
              { label: 'Getting Started', to: '/getting-started/setup' },
              { label: 'Backend', to: '/backend/project-structure' },
            ],
          },
          {
            title: 'Quick Links',
            items: [
              { label: 'API Reference', to: '/backend/api-reference' },
              { label: 'SOPs', to: '/sops/adding-new-feature' },
              { label: 'Scripts', to: '/scripts/reference' },
            ],
          },
        ],
        copyright: `Financial Agent Documentation · Built with Docusaurus`,
      },
      prism: {
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
        additionalLanguages: ['bash', 'python', 'json', 'ini'],
      },
    }),
};

export default config;
