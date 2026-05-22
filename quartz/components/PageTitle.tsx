import { pathToRoot } from "../util/path"
import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"
import { classNames } from "../util/lang"

const PageTitle: QuartzComponent = ({ fileData, displayClass }: QuartzComponentProps) => {
  const baseDir = pathToRoot(fileData.slug!)
  return (
    <div class={classNames(displayClass, "page-title")}>
      <a href={baseDir} aria-label="The English Nobel — home">
        <img
          src="/static/ten-logo-monogram.svg"
          alt="TEN"
          width="180"
          height="180"
          class="ten-monogram"
        />
      </a>
    </div>
  )
}

PageTitle.css = `
.page-title {
  margin: 0 0 0.5rem 0;
  line-height: 0;
  display: flex;
  justify-content: center;
}
.page-title a {
  display: inline-block;
  text-decoration: none;
  line-height: 0;
}
.ten-monogram {
  display: block;
  width: 180px !important;
  height: 180px !important;
  margin: 0 !important;
}
`

export default (() => PageTitle) satisfies QuartzComponentConstructor
