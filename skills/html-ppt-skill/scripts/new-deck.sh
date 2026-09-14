#!/usr/bin/env bash
# html-ppt :: new-deck.sh — scaffold a new deck from a template
#
# Usage:
#   new-deck.sh <name> [output-parent-dir] [-t <template>]
#
# Creates <parent>/<name>/index.html with the asset references rewritten so
# they resolve from wherever the deck actually lands — at any depth, inside
# the skill tree or outside it.
#
#   <output-parent-dir>  absolute, or relative to the current directory.
#                        Defaults to <skill>/examples.
#   -t, --template       "deck" (default), a full-deck name (e.g. pitch-deck),
#                        a single-page name (e.g. arch-diagram), or a path to
#                        any .html file / full-deck directory.

set -euo pipefail

HERE="$(cd "$(dirname "$0")/.." && pwd)"

NAME=""
PARENT=""
TEMPLATE_ARG="deck"

while [[ $# -gt 0 ]]; do
  case "$1" in
    -t|--template)
      TEMPLATE_ARG="${2:-}"
      if [[ -z "$TEMPLATE_ARG" ]]; then
        echo "error: --template needs a value" >&2
        exit 1
      fi
      shift 2
      ;;
    -h|--help)
      sed -n '3,15p' "$0" | sed 's|^# \{0,1\}||'
      exit 0
      ;;
    -*)
      echo "error: unknown option $1" >&2
      exit 1
      ;;
    *)
      if [[ -z "$NAME" ]]; then
        NAME="$1"
      elif [[ -z "$PARENT" ]]; then
        PARENT="$1"
      else
        echo "error: unexpected argument $1" >&2
        exit 1
      fi
      shift
      ;;
  esac
done

if [[ -z "$NAME" ]]; then
  echo "usage: new-deck.sh <name> [parent-dir] [-t <template>]" >&2
  exit 1
fi

# ---------------------------------------------------------------- template
# Accept a bare name (deck / a full-decks dir / a single-page layout) or an
# explicit path. A full-deck resolves to a directory and is copied whole.
resolve_template() {
  local t="$1"
  if [[ -e "$t" ]]; then printf '%s' "$t"; return; fi
  if [[ "$t" == "deck" && -f "$HERE/templates/deck.html" ]]; then
    printf '%s' "$HERE/templates/deck.html"; return
  fi
  if [[ -d "$HERE/templates/full-decks/$t" ]]; then
    printf '%s' "$HERE/templates/full-decks/$t"; return
  fi
  if [[ -f "$HERE/templates/single-page/$t.html" ]]; then
    printf '%s' "$HERE/templates/single-page/$t.html"; return
  fi
  if [[ -f "$HERE/templates/$t" ]]; then
    printf '%s' "$HERE/templates/$t"; return
  fi
  return 1
}

if ! TEMPLATE="$(resolve_template "$TEMPLATE_ARG")"; then
  echo "error: no template named '$TEMPLATE_ARG'" >&2
  echo "  full-decks:   $(ls "$HERE/templates/full-decks" 2>/dev/null | tr '\n' ' ')" >&2
  echo "  single-page:  see $HERE/templates/single-page/" >&2
  exit 1
fi

# ------------------------------------------------------------------ output
# Absolute parent is honoured as-is; a relative one resolves against the
# caller's current directory, which is what a shell user expects. Only the
# default lives inside the skill.
if [[ -z "$PARENT" ]]; then
  PARENT_ABS="$HERE/examples"
elif [[ "$PARENT" == /* ]]; then
  PARENT_ABS="$PARENT"
else
  PARENT_ABS="$PWD/$PARENT"
fi

OUT_DIR="$PARENT_ABS/$NAME"
if [[ -e "$OUT_DIR" ]]; then
  echo "error: $OUT_DIR already exists" >&2
  exit 1
fi
mkdir -p "$OUT_DIR"
OUT_DIR="$(cd "$OUT_DIR" && pwd)"   # normalise ., .., symlinks

# ---------------------------------------------------------------- rel path
# Relative path from the deck directory back to the skill root, so the asset
# links are correct at any depth and from outside the skill tree.
relpath() {
  local target="${1%/}" base="${2%/}" up="" rest
  while [[ "$base" != "/" && "$target" != "$base" && "$target" != "$base"/* ]]; do
    base="$(dirname "$base")"
    up="../$up"
  done
  rest="${target#"$base"}"
  rest="${rest#/}"
  up="${up%/}"
  if [[ -z "$up" ]]; then printf '%s' "${rest:-.}"
  elif [[ -z "$rest" ]]; then printf '%s' "$up"
  else printf '%s/%s' "$up" "$rest"
  fi
}

REL="$(relpath "$HERE" "$OUT_DIR")"

# Rewrite any run of ../ in front of assets/ to the computed prefix, so the
# same logic works for templates/deck.html (../assets/), single-page
# (../../assets/) and full-decks (../../../assets/) alike.
rewrite_assets() {
  local file="$1"
  sed -E -i.bak "s#([\"'(])(\.\./)*assets/#\1${REL}/assets/#g" "$file"
  rm -f "$file.bak"
}

if [[ -d "$TEMPLATE" ]]; then
  cp -R "$TEMPLATE/." "$OUT_DIR/"
  while IFS= read -r f; do rewrite_assets "$f"; done \
    < <(find "$OUT_DIR" -type f \( -name '*.html' -o -name '*.css' -o -name '*.js' \))
else
  cp "$TEMPLATE" "$OUT_DIR/index.html"
  rewrite_assets "$OUT_DIR/index.html"
fi

if [[ ! -f "$OUT_DIR/index.html" ]]; then
  echo "error: template produced no index.html in $OUT_DIR" >&2
  exit 1
fi

# Join a relative reference onto a directory the way a browser resolves it
# against a file:// URL: purely lexically. The shell's own ".." follows
# symlinks instead (/tmp -> /private/tmp), which would disagree.
lexjoin() {
  local p="$1/$2" out="" seg oldifs="$IFS"
  set -f; IFS='/'
  for seg in $p; do
    case "$seg" in
      ''|.) ;;
      ..)   out="${out%/*}" ;;
      *)    out="$out/$seg" ;;
    esac
  done
  IFS="$oldifs"; set +f
  printf '%s' "${out:-/}"
}

# Self-check: every asset href/src must resolve to a real file. A broken path
# here is exactly the bug this script used to ship (#19) — fail loudly.
MISSING=0
while IFS= read -r ref; do
  if [[ ! -e "$(lexjoin "$OUT_DIR" "$ref")" ]]; then
    echo "error: unresolved asset reference: $ref" >&2
    MISSING=1
  fi
done < <(grep -oE "[\"'](\.\./)*[^\"']*assets/[^\"']+" "$OUT_DIR/index.html" \
           | sed -E "s/^[\"']//" | sort -u)
[[ $MISSING -eq 0 ]] || exit 1

echo "✔ created $OUT_DIR/index.html"
echo "  template: $TEMPLATE"
echo "  assets:   $REL/assets/  (verified)"
echo ""
echo "next steps:"
echo "  open  $OUT_DIR/index.html"
echo "  # press T to cycle themes, ← → to navigate, O for overview"
echo ""
echo "  # render to PNG:"
echo "  $HERE/scripts/render.sh $OUT_DIR/index.html all"
