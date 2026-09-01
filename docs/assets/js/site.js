(function () {
  "use strict";

  function normalize(value) {
    return (value || "")
      .toString()
      .trim()
      .toLowerCase()
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "");
  }

  function formatTemplate(template, values) {
    return Object.keys(values).reduce(function (result, key) {
      return result.split("{" + key + "}").join(values[key]);
    }, template || "");
  }

  function initResourceFinder() {
    var finder = document.querySelector("[data-resource-finder]");
    if (!finder) return;

    var results = document.querySelector("[data-resource-results]");
    var cards = results ? Array.from(results.querySelectorAll("[data-resource-card]")) : [];
    var search = finder.querySelector("[data-filter-search]");
    var controls = Array.from(finder.querySelectorAll("[data-filter]"));
    var count = finder.querySelector("[data-result-count]");
    var empty = document.querySelector("[data-resource-empty]");
    var reset = finder.querySelector("[data-filter-reset]");

    function currentFilters() {
      var filters = {};
      controls.forEach(function (control) {
        filters[control.getAttribute("data-filter")] = normalize(control.value);
      });
      return filters;
    }

    function updateUrl(filters, query) {
      var params = new URLSearchParams();
      if (query) params.set("q", query);
      Object.keys(filters).forEach(function (key) {
        if (filters[key]) params.set(key, filters[key]);
      });
      var next = window.location.pathname + (params.toString() ? "?" + params.toString() : "") + "#resource-finder";
      window.history.replaceState(null, "", next);
    }

    function applyFilters(updateHistory) {
      var query = normalize(search && search.value);
      var filters = currentFilters();
      var visible = 0;

      cards.forEach(function (card) {
        var haystack = [
          card.getAttribute("data-title"),
          card.getAttribute("data-summary"),
          card.getAttribute("data-topic"),
          card.getAttribute("data-source")
        ].join(" ");
        var matchesQuery = !query || haystack.indexOf(query) !== -1;
        var matchesFilters = Object.keys(filters).every(function (key) {
          return !filters[key] || normalize(card.getAttribute("data-" + key)) === filters[key];
        });
        var show = matchesQuery && matchesFilters;
        card.hidden = !show;
        if (show) visible += 1;
      });

      if (count) {
        count.textContent = visible + (visible === 1 ? " resource" : " resources");
      }
      if (empty) {
        empty.hidden = visible !== 0;
      }
      if (updateHistory) {
        updateUrl(filters, query);
      }
    }

    function restoreFromUrl() {
      var params = new URLSearchParams(window.location.search);
      if (search && params.has("q")) search.value = params.get("q");
      controls.forEach(function (control) {
        var key = control.getAttribute("data-filter");
        if (params.has(key)) control.value = params.get(key);
      });
    }

    restoreFromUrl();
    applyFilters(false);

    if (search) {
      search.addEventListener("input", function () {
        applyFilters(true);
      });
    }
    controls.forEach(function (control) {
      control.addEventListener("change", function () {
        applyFilters(true);
      });
    });
    if (reset) {
      reset.addEventListener("click", function () {
        if (search) search.value = "";
        controls.forEach(function (control) {
          control.value = "";
        });
        applyFilters(true);
        if (search) search.focus();
      });
    }
  }

  function initCategoryFinders() {
    document.querySelectorAll("[data-category-finder]").forEach(function (finder) {
      var queryInput = finder.querySelector("[data-category-query]");
      var reset = finder.querySelector("[data-category-reset]");
      var status = finder.querySelector("[data-category-status]");
      var empty = finder.querySelector("[data-category-empty]");
      var tiles = Array.from(finder.querySelectorAll("[data-category-tile]"));
      var queryParam = "resource_q";

      function updateUrl(rawQuery) {
        var params = new URLSearchParams(window.location.search);
        if (rawQuery) {
          params.set(queryParam, rawQuery);
        } else {
          params.delete(queryParam);
        }
        var next = window.location.pathname + (params.toString() ? "?" + params.toString() : "") + window.location.hash;
        window.history.replaceState(null, "", next);
      }

      function applyFilters(updateHistory) {
        var rawQuery = (queryInput && queryInput.value || "").trim();
        var query = normalize(rawQuery);
        var visibleItems = 0;
        var visibleTiles = 0;

        tiles.forEach(function (tile) {
          var tileHeader = tile.querySelector(".category-tile__header");
          var categoryTitle = tileHeader && tileHeader.querySelector("h3");
          var categoryHaystack = categoryTitle && categoryTitle.textContent;
          var categoryMatches = Boolean(query && normalize(categoryHaystack).indexOf(query) !== -1);
          var tileVisibleItems = 0;
          var items = Array.from(tile.querySelectorAll("[data-category-item]"));

          items.forEach(function (item) {
            var itemHaystack = [
              item.getAttribute("data-search"),
              item.textContent
            ].join(" ");
            var show = !query || categoryMatches || normalize(itemHaystack).indexOf(query) !== -1;
            item.hidden = !show;
            if (show) {
              tileVisibleItems += 1;
              visibleItems += 1;
            }
          });

          tile.querySelectorAll("[data-category-group]").forEach(function (group) {
            group.hidden = !group.querySelector("[data-category-item]:not([hidden])");
          });

          tile.hidden = tileVisibleItems === 0;
          if (!tile.hidden) visibleTiles += 1;
        });

        if (status) {
          var resourceLabel = visibleItems === 1 ? "resource" : "resources";
          var categoryLabel = visibleTiles === 1 ? "category" : "categories";
          status.textContent = visibleItems + " " + resourceLabel + " across " + visibleTiles + " " + categoryLabel;
        }
        if (empty) empty.hidden = visibleItems !== 0;
        if (reset) reset.disabled = !rawQuery;
        if (updateHistory) updateUrl(rawQuery);
      }

      var params = new URLSearchParams(window.location.search);
      if (queryInput && params.has(queryParam)) {
        queryInput.value = params.get(queryParam);
      }
      applyFilters(false);

      if (queryInput) {
        queryInput.addEventListener("input", function () {
          applyFilters(true);
        });
        queryInput.addEventListener("keydown", function (event) {
          if (event.key !== "Escape" || !queryInput.value) return;
          queryInput.value = "";
          applyFilters(true);
        });
      }
      if (reset) {
        reset.addEventListener("click", function () {
          if (queryInput) {
            queryInput.value = "";
            queryInput.focus();
          }
          applyFilters(true);
        });
      }
    });
  }

  function initReleaseFinders() {
    document.querySelectorAll("[data-release-finder]").forEach(function (finder) {
      var root = finder.closest(".release-history");
      if (!root) return;

      var queryInput = finder.querySelector("[data-release-query]");
      var versionSelect = finder.querySelector("[data-release-version-filter]");
      var reset = finder.querySelector("[data-release-reset]");
      var count = finder.querySelector("[data-release-result-count]");
      var empty = root.querySelector("[data-release-empty]");
      var timeline = root.querySelector("[data-release-timeline]");
      var jump = root.querySelector("[data-release-jump]");
      var jumpLinks = jump ? Array.from(jump.querySelectorAll("[data-release-jump-version]")) : [];
      var entries = Array.from(root.querySelectorAll("[data-release-entry]"));
      var entriesByVersion = {};
      var product = finder.getAttribute("data-release-product") || "";
      var queryParam = finder.getAttribute("data-release-query-param") || "release_q";
      var versionParam = finder.getAttribute("data-release-version-param") || "release_version";
      var anchor = finder.getAttribute("data-release-anchor") || "latest-releases";
      var labels = {
        matches: finder.getAttribute("data-label-matches") || "Matching feature references",
        changes: finder.getAttribute("data-label-changes") || "Documented changes",
        releases: finder.getAttribute("data-label-releases") || "Releases",
        version: finder.getAttribute("data-label-version") || "Version",
        emptyVersion: finder.getAttribute("data-empty-version") || "No documented feature matching “{query}” was found for {product} version {version}.",
        emptyAll: finder.getAttribute("data-empty-all") || "No documented feature matching “{query}” was found in the available {product} releases."
      };

      entries.forEach(function (entry) {
        entriesByVersion[entry.getAttribute("data-release-version")] = entry;
      });

      function updateUrl(rawQuery, version) {
        var params = new URLSearchParams(window.location.search);
        if (rawQuery) {
          params.set(queryParam, rawQuery);
        } else {
          params.delete(queryParam);
        }
        if (version) {
          params.set(versionParam, version);
        } else {
          params.delete(versionParam);
        }
        var next = window.location.pathname + (params.toString() ? "?" + params.toString() : "") + "#" + anchor;
        window.history.replaceState(null, "", next);
      }

      function applyFilters(updateHistory) {
        var rawQuery = (queryInput && queryInput.value || "").trim();
        var query = normalize(rawQuery);
        var version = versionSelect ? versionSelect.value : "";
        var filtering = Boolean(query || version);
        var totalChanges = 0;
        var totalMatches = 0;
        var visibleReleases = 0;

        entries.forEach(function (entry) {
          var entryVersion = entry.getAttribute("data-release-version");
          var versionMatches = !version || entryVersion === version;
          var details = entry.querySelector("[data-release-details]");
          var highlightsSection = entry.querySelector("[data-release-highlights]");
          var highlights = Array.from(entry.querySelectorAll("[data-release-highlight]"));
          var changes = Array.from(entry.querySelectorAll("[data-release-change]"));
          var categories = Array.from(entry.querySelectorAll("[data-release-category]"));
          var matchingHighlights = 0;
          var matchingChanges = 0;

          highlights.forEach(function (highlight) {
            var matches = !query || normalize(highlight.getAttribute("data-search")).indexOf(query) !== -1;
            highlight.hidden = Boolean(query && !matches);
            if (query && matches) matchingHighlights += 1;
          });
          if (highlightsSection) {
            highlightsSection.hidden = Boolean(query && matchingHighlights === 0);
          }

          changes.forEach(function (change) {
            var matches = !query || normalize(change.getAttribute("data-search")).indexOf(query) !== -1;
            change.hidden = Boolean(query && !matches);
            if (matches) matchingChanges += 1;
          });

          categories.forEach(function (category) {
            category.hidden = Boolean(query && !category.querySelector("[data-release-change]:not([hidden])"));
          });

          var queryMatches = !query || matchingChanges > 0 || matchingHighlights > 0;
          var show = versionMatches && queryMatches;
          entry.hidden = !show;

          if (show) {
            visibleReleases += 1;
            totalChanges += changes.length;
            totalMatches += query ? matchingChanges + matchingHighlights : changes.length;
          }

          if (details) {
            details.hidden = Boolean(query && matchingChanges === 0);
            if (query && show && matchingChanges > 0) {
              if (!details.open) {
                details.open = true;
                details.setAttribute("data-release-auto-opened", "true");
              }
            } else if (details.getAttribute("data-release-auto-opened") === "true") {
              details.open = false;
              details.removeAttribute("data-release-auto-opened");
            }
          }
        });

        jumpLinks.forEach(function (link) {
          var entry = entriesByVersion[link.getAttribute("data-release-jump-version")];
          link.hidden = !entry || entry.hidden;
        });

        if (timeline) timeline.hidden = visibleReleases === 0;
        if (jump) jump.hidden = visibleReleases === 0;

        var releaseScope = version
          ? labels.version + ": " + version
          : labels.releases + ": " + visibleReleases;
        if (count) {
          if (query) {
            count.textContent = labels.matches + ": " + totalMatches + " · " + releaseScope;
          } else {
            count.textContent = labels.changes + ": " + totalChanges + " · " + releaseScope;
          }
        }

        if (empty) {
          empty.hidden = visibleReleases !== 0;
          if (visibleReleases === 0) {
            empty.textContent = formatTemplate(version ? labels.emptyVersion : labels.emptyAll, {
              product: product,
              query: rawQuery,
              version: version
            });
          }
        }

        if (reset) reset.disabled = !filtering;
        if (updateHistory) updateUrl(rawQuery, version);
      }

      function restoreFromUrl() {
        var params = new URLSearchParams(window.location.search);
        if (queryInput && params.has(queryParam)) queryInput.value = params.get(queryParam);
        if (versionSelect && params.has(versionParam)) versionSelect.value = params.get(versionParam);
      }

      restoreFromUrl();
      applyFilters(false);

      if (queryInput) {
        queryInput.addEventListener("input", function () {
          applyFilters(true);
        });
      }
      if (versionSelect) {
        versionSelect.addEventListener("change", function () {
          applyFilters(true);
        });
      }
      if (reset) {
        reset.addEventListener("click", function () {
          if (queryInput) queryInput.value = "";
          if (versionSelect) versionSelect.value = "";
          applyFilters(true);
          if (queryInput) queryInput.focus();
        });
      }
    });
  }

  function initCopyButtons() {
    document.querySelectorAll(".copy-btn, [data-copy-button]").forEach(function (button) {
      if (button.dataset.copyReady === "true") return;
      button.dataset.copyReady = "true";
      button.setAttribute("aria-label", button.getAttribute("aria-label") || "Copy code sample");

      button.addEventListener("click", function () {
        var targetId = button.getAttribute("data-copy-target");
        var target = targetId ? document.getElementById(targetId) : button.parentElement.querySelector("pre");
        if (!target || !navigator.clipboard) {
          button.textContent = "Copy unavailable";
          return;
        }

        navigator.clipboard.writeText(target.textContent.trim()).then(function () {
          var original = button.getAttribute("data-copy-label") || "Copy";
          button.textContent = "Copied!";
          button.classList.add("copied");
          window.setTimeout(function () {
            button.textContent = original;
            button.classList.remove("copied");
          }, 1600);
        }).catch(function () {
          button.textContent = "Copy failed";
        });
      });
    });
  }

  function initLinkIndicators() {
    document.querySelectorAll("a[href]").forEach(function (link) {
      var rawHref = link.getAttribute("href");
      if (
        !rawHref ||
        rawHref.charAt(0) === "#" ||
        rawHref.indexOf("mailto:") === 0 ||
        rawHref.indexOf("tel:") === 0 ||
        rawHref.indexOf("javascript:") === 0
      ) return;

      var url;
      try {
        url = new URL(link.href, window.location.href);
      } catch (error) {
        console.warn("Could not inspect link URL.", rawHref, error);
        return;
      }

      var isHttp = url.protocol === "http:" || url.protocol === "https:";
      var isExternal = isHttp && url.origin !== window.location.origin;
      if (isExternal) {
        var rel = new Set((link.getAttribute("rel") || "").split(/\s+/).filter(Boolean));
        rel.add("noopener");
        rel.add("noreferrer");
        link.setAttribute("target", "_blank");
        link.setAttribute("rel", Array.from(rel).join(" "));
      }

      if (link.querySelector(".link-indicator") || link.hasAttribute("data-no-link-indicator")) return;
      var isDocument = /\.(pdf|docx?|xlsx?|pptx?)(?:$|[?#])/i.test(url.pathname);
      if (!isExternal && !isDocument) return;

      var indicator = document.createElement("span");
      indicator.className = "link-indicator";
      indicator.setAttribute("aria-hidden", "true");
      indicator.textContent = isDocument ? "PDF" : "↗";
      link.appendChild(indicator);
    });
  }

  function initVideoLibraries() {
    document.querySelectorAll("[data-video-library]").forEach(function (library) {
      var rows = Array.from(library.querySelectorAll("[data-video-row]"));
      var search = library.querySelector("[data-video-search]");
      var filters = Array.from(library.querySelectorAll("[data-video-filter]"));
      var duration = library.querySelector("[data-video-duration]");
      var count = library.querySelector("[data-video-count]");
      var empty = library.querySelector("[data-video-empty]");
      var reset = library.querySelector("[data-video-reset]");
      var sections = Array.from(library.querySelectorAll(".video-section"));

      function durationMatches(row, value) {
        if (!value) return true;
        var minutes = Number(row.getAttribute("data-duration"));
        if (!minutes) return false;
        if (value === "short") return minutes <= 15;
        if (value === "medium") return minutes >= 16 && minutes <= 30;
        return minutes > 30;
      }

      function updateUrl(query, activeFilters, durationValue) {
        var params = new URLSearchParams();
        if (query) params.set("video_q", query);
        Object.keys(activeFilters).forEach(function (key) {
          if (activeFilters[key]) params.set("video_" + key, activeFilters[key]);
        });
        if (durationValue) params.set("video_duration", durationValue);
        var next = window.location.pathname + (params.toString() ? "?" + params.toString() : "");
        window.history.replaceState(null, "", next);
      }

      function applyFilters(updateHistory) {
        var query = normalize(search && search.value);
        var activeFilters = {};
        filters.forEach(function (control) {
          activeFilters[control.getAttribute("data-video-filter")] = normalize(control.value);
        });
        var durationValue = normalize(duration && duration.value);
        var visible = 0;

        rows.forEach(function (row) {
          var haystack = [
            row.getAttribute("data-search"),
            row.getAttribute("data-source"),
            row.getAttribute("data-language")
          ].join(" ");
          var matchesQuery = !query || normalize(haystack).indexOf(query) !== -1;
          var matchesFilters = Object.keys(activeFilters).every(function (key) {
            return !activeFilters[key] || normalize(row.getAttribute("data-" + key)) === activeFilters[key];
          });
          var show = matchesQuery && matchesFilters && durationMatches(row, durationValue);
          row.hidden = !show;
          if (show) visible += 1;
        });

        sections.forEach(function (section) {
          section.hidden = !section.querySelector("[data-video-row]:not([hidden])");
        });
        if (count) count.textContent = visible + (visible === 1 ? " video" : " videos");
        if (empty) empty.hidden = visible !== 0;
        if (updateHistory) updateUrl(query, activeFilters, durationValue);
      }

      function restoreFromUrl() {
        var params = new URLSearchParams(window.location.search);
        if (search && params.has("video_q")) search.value = params.get("video_q");
        filters.forEach(function (control) {
          var key = "video_" + control.getAttribute("data-video-filter");
          if (params.has(key)) control.value = params.get(key);
        });
        if (duration && params.has("video_duration")) duration.value = params.get("video_duration");
      }

      restoreFromUrl();
      applyFilters(false);

      if (search) search.addEventListener("input", function () { applyFilters(true); });
      filters.forEach(function (control) {
        control.addEventListener("change", function () { applyFilters(true); });
      });
      if (duration) duration.addEventListener("change", function () { applyFilters(true); });
      if (reset) {
        reset.addEventListener("click", function () {
          if (search) search.value = "";
          filters.forEach(function (control) { control.value = ""; });
          if (duration) duration.value = "";
          applyFilters(true);
          if (search) search.focus();
        });
      }

      library.querySelectorAll("[data-video-sort]").forEach(function (button) {
        button.addEventListener("click", function () {
          var table = document.getElementById(button.getAttribute("data-table"));
          if (!table) return;
          var key = button.getAttribute("data-video-sort");
          var body = table.querySelector("tbody");
          var tableRows = Array.from(body.querySelectorAll("[data-video-row]"));
          var direction = button.getAttribute("data-direction") === "asc" ? "desc" : "asc";

          table.querySelectorAll("[data-video-sort]").forEach(function (other) {
            other.removeAttribute("data-direction");
            other.closest("th").setAttribute("aria-sort", "none");
          });
          button.setAttribute("data-direction", direction);
          button.closest("th").setAttribute("aria-sort", direction === "asc" ? "ascending" : "descending");

          tableRows.sort(function (left, right) {
            var leftValue = left.getAttribute("data-" + key) || "";
            var rightValue = right.getAttribute("data-" + key) || "";
            var comparison;
            if (key === "number" || key === "duration") {
              comparison = Number(leftValue) - Number(rightValue);
            } else {
              comparison = leftValue.localeCompare(rightValue);
            }
            return direction === "asc" ? comparison : -comparison;
          });
          tableRows.forEach(function (row) { body.appendChild(row); });
        });
      });
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    initResourceFinder();
    initCategoryFinders();
    initReleaseFinders();
    initCopyButtons();
    initLinkIndicators();
    initVideoLibraries();
  });
})();
