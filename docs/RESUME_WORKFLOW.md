# Editing and publishing your resume

Your public resume is `resume/Vaishnav_AK_DS_AI_ATS.pdf`. Its LaTeX source is `resume/vaishnav_DS_AI_ats.tex`.

## Edit in Overleaf

1. Create an Overleaf project and upload `vaishnav_DS_AI_ats.tex`.
2. Select pdfLaTeX as the compiler. The source uses standard packages and requires no external images or custom font files.
3. Edit the project and recompile. Check page breaks, text selection, and links in the resulting PDF.
4. Use a separate Overleaf project copy for a tailored application version. Keep the general portfolio resume as the public default.
5. Download the selected PDF and replace `resume/Vaishnav_AK_DS_AI_ATS.pdf` in this repository. Update the `.tex` source alongside it so the two stay in sync.
6. Preview the resume page locally, then publish through the normal site deployment.

There is no automatic connection between Overleaf and GitHub Pages. Editing an Overleaf draft does not change the public site until the exported PDF is committed and deployed.

The website's HTML career summary is stored in `_data/portfolio.json`. If a resume edit changes your role, dates, experience, or education, update that data too. Case-study content lives in `_data/case_studies.json`.

The older `assets/Vaishnav_Ak_Resume.pdf` remains a legacy file for existing links. It is not the new resume page's default document.

Do not add private application drafts or employer information that is not intended for public release to this public repository.

Overleaf references: [uploading projects](https://www.overleaf.com/learn/latex/Kb/Uploading_a_project) and [downloading source and PDF](https://docs.overleaf.com/managing-projects-and-files/downloading-a-project).
