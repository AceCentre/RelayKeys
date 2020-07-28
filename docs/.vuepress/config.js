module.exports = {
  base: '/RelayKeys/',
  title: 'RelayKeys Docs',
  description: 'Emulate a Keyboard and Mouse with a computer',
  ga: 'UA-24637628-7',
  plugins: [
    '@vuepress/medium-zoom', 'vuepress-plugin-export'
  ],
  head: [
    ['link', { rel: "manifest",  href: "/site.webmanifest" }],
    ['link', { rel: "mask-icon",  href: "/safari-pinned-tab.svg", color: "#5bbad5" }],
    ['link', { rel: "shortcut icon", type: "image/x-icon", href: "/favicon.ico" }],
    ['link', { rel: "apple-touch-icon", type: "image/x-icon", sizes: "180x180", href: "/apple-touch-icon.png" }],
    ['link', { rel: "icon", type: "image/png", sizes: "32x32", href: "/favicon-32x32.png" }],
    ['link', { rel: "icon", type: "image/png", sizes: "16x16", href: "/favicon-16x16.png" }],
    ['meta', { name: "application-name", content: "RelayKeys Docs" }],
    ['meta', { name: "theme-color", content: "#263238" }],
    ['meta', { name: "apple-mobile-web-app-title", content: "Directus Docs" }],
    ['meta', { name: "msapplication-TileColor", content: "#263238" }],
    ['meta', { name: "msapplication-config", content: "/browserconfig.xml" }]
  ],
  themeConfig: {
    lastUpdated: 'Last Updated',
    repo: 'acecentre/relaykeys',
    docsDir: 'docs',
    logo: '/img/AceLogo.png',
    editLinks: true,
    serviceWorker: true,
    hiddenLinks: [],
    nav: [
      { text: 'AceCentre', link: 'https://acecentre.org.uk' },
    ],
    sidebarDepth: 1,
    // ⌨️ 🧠 📡 🤖 ✨ 💥 🔥 🌈 ⭐️ 🍄 🍹 🎱 🎨 🏆 🚨 🚀 💡 ⚙️ 🔮 🛠 🔑 🎁 🎈 🎀 ❤️ 💯
    sidebar: [
      {
        title: '⌨️ Getting Started',
        collapsable: false,
        children: [
          ['/getting-started/introduction', 'Introduction'],
          ['/getting-started/installation', 'Installation'],
          ['/getting-started/supporting-relaykeys', 'Supporting RelayKeys'],
          ['/getting-started/troubleshooting', 'Troubleshooting'],
        ]
      },
      {
        title: '📖 AAC Integration Guides',
        collapsable: true,
        children: [
          ['/guides/basic-principles', 'Basic Principles'],
          ['/guides/communicator', 'Tobii - Communicator'], 
          ['/guides/grid3', 'Smartbox - The Grid3'], 
          ['/guides/mindexpress', 'Jabbla - MindExpress'], 
          ['/guides/snap-corefirst', 'Tobii Dynavox - Snap & Corefirst' ]
        ]
      },
      {
        title: '🚀 Command Line Interface (CLI) Details',
        collapsable: true,
        children: [
          '/cli/reference'
        ]
      },
      {
        title: '⚡️ Development Guide',
        collapsable: true,
        children: [
          ['/developers/architecture', 'Architecture and Getting started'],
          ['/developers/supported-boards', 'Supported Boards and Build Instructions'],
          ['/developers/reference', 'RPC Daemon Details'],
          ['/developers/relaykeys-cfg', 'Config file details'],
          ['/developers/other-projects', 'Other Projects'],
          ['/developers/credits', 'Credits'],
          ['/developers/contributing', 'Contributing']
        ]
      },
    ]
  }
};