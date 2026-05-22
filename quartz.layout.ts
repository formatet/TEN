import { PageLayout, SharedLayout } from "./quartz/cfg"
import * as Component from "./quartz/components"

function explorerSort(a: any, b: any): number {
  const FOLDER_ORDER = ["CHAPTERS", "THE-GALLERY", "THE-ARCHIVE"]

  const aIsFolder = a.file === null
  const bIsFolder = b.file === null

  if (aIsFolder && bIsFolder) {
    const slug = (n: any) => (n.slugSegment || n.displayName || "").toUpperCase().replace(/\s+/g, "-")
    const aIdx = FOLDER_ORDER.indexOf(slug(a))
    const bIdx = FOLDER_ORDER.indexOf(slug(b))
    if (aIdx >= 0 && bIdx >= 0) return aIdx - bIdx
    return (a.displayName || "").localeCompare(b.displayName || "")
  }

  if (aIsFolder) return -1
  if (bIsFolder) return 1

  // Kapitelnummer ur slugSegment: "Chapter-1-The-..." → 1
  const segA = (a.slugSegment || "") as string
  const segB = (b.slugSegment || "") as string
  const chA = segA.match(/Chapter.?(\d+)/i)
  const chB = segB.match(/Chapter.?(\d+)/i)
  if (chA && chB) return parseInt(chA[1]) - parseInt(chB[1])

  return (a.displayName || "").localeCompare(b.displayName || "")
}

export const sharedPageComponents: SharedLayout = {
  head: Component.Head(),
  header: [],
  afterBody: [],
  footer: Component.Footer({ links: {} }),
}

export const defaultContentPageLayout: PageLayout = {
  beforeBody: [Component.ArticleTitle()],
  left: [
    Component.PageTitle(),
    Component.MobileOnly(Component.Spacer()),
    Component.Search(),
    Component.Explorer({
      title: "",
      folderClickBehavior: "collapse",
      folderDefaultState: "open",
      useSavedState: false,
      sortFn: explorerSort,
    }),
  ],
  right: [Component.DesktopOnly(Component.TableOfContents())],
  afterBody: [Component.Backlinks(), Component.WiktionaryLookup(), Component.TENTracking()],
}

export const defaultListPageLayout: PageLayout = {
  beforeBody: [Component.ArticleTitle()],
  left: [
    Component.PageTitle(),
    Component.MobileOnly(Component.Spacer()),
    Component.Search(),
    Component.Explorer({
      title: "",
      folderClickBehavior: "collapse",
      folderDefaultState: "open",
      useSavedState: false,
      sortFn: explorerSort,
    }),
  ],
  right: [],
}
