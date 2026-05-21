import { QuartzConfig } from "./quartz/cfg"
import * as Plugin from "./quartz/plugins"

const config: QuartzConfig = {
  configuration: {
    pageTitle: "The English Nobel",
    pageTitleSuffix: "",
    enableSPA: true,
    enablePopovers: true,
    analytics: {
      provider: "umami",
      websiteId: "bc585229-b7c7-4acc-946c-ac3973020601",
      host: "https://s.kristall.info",
    },
    locale: "en-US",
    baseUrl: "ten.formatet.se",
    ignorePatterns: ["private", "templates", ".obsidian"],
    defaultDateType: "modified",
    theme: {
      fontOrigin: "local",
      cdnCaching: true,
      typography: {
        header: "EB Garamond",
        body:   "EB Garamond",
        code: "JetBrains Mono",
      },
      colors: {
        lightMode: {
          light: "#F4EFE3",
          lightgray: "#E5DFD0",
          gray: "#6B6760",
          darkgray: "#2A2826",
          dark: "#1a1a1a",
          secondary: "#1a1a1a",
          tertiary: "#6B6760",
          highlight: "rgba(26,26,26,0.05)",
          textHighlight: "rgba(218,196,128,0.28)",
        },
        darkMode: {
          light: "#161618",
          lightgray: "#393639",
          gray: "#646464",
          darkgray: "#d4d4d4",
          dark: "#ebebec",
          secondary: "#c8b99a",
          tertiary: "#9e8f7a",
          highlight: "rgba(200,185,154,0.08)",
          textHighlight: "rgba(218,196,128,0.2)",
        },
      },
    },
  },
  plugins: {
    transformers: [
      Plugin.FrontMatter(),
      Plugin.CreatedModifiedDate({
        priority: ["frontmatter", "git", "filesystem"],
      }),
      Plugin.SyntaxHighlighting({
        theme: { light: "github-light", dark: "github-dark" },
        keepBackground: false,
      }),
      Plugin.ObsidianFlavoredMarkdown({ enableInHtmlEmbed: false }),
      Plugin.GitHubFlavoredMarkdown(),
      Plugin.TableOfContents(),
      Plugin.CrawlLinks({ markdownLinkResolution: "shortest" }),
      Plugin.Description(),
    ],
    filters: [Plugin.RemoveDrafts()],
    emitters: [
      Plugin.AliasRedirects(),
      Plugin.ComponentResources(),
      Plugin.ContentPage(),
      Plugin.FolderPage(),
      Plugin.TagPage(),
      Plugin.ContentIndex({ enableSiteMap: true, enableRSS: false }),
      Plugin.Assets(),
      Plugin.Static(),
      Plugin.Favicon(),
      Plugin.NotFoundPage(),
    ],
  },
}

export default config
