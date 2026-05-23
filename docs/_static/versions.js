/* worktoy docs: version switcher.
 *
 * The multi-version GitHub Pages build writes a 'versions.json' at the
 * site root (e.g. ["latest", "0.99.137", ...]) and serves each version
 * under '<root>/<version>/'. This script finds that file by walking up
 * from the current page (so it does not need to know the Pages base
 * path), builds a dropdown of versions, and navigates to the chosen
 * one. On a local single-version build there is no versions.json, the
 * fetch fails, and nothing is shown. */

(function () {
  "use strict";

  var CANDIDATES = [
    "versions.json",
    "../versions.json",
    "../../versions.json",
    "../../../versions.json",
    "../../../../versions.json",
    "../../../../../versions.json"
  ];

  function findVersions(index) {
    if (index >= CANDIDATES.length) {
      return Promise.reject();
    }
    var rel = CANDIDATES[index];
    return fetch(rel).then(function (response) {
      if (!response.ok) {
        throw new Error("not here");
      }
      return response.json().then(function (versions) {
        return {base: rel.replace(/versions\.json$/, ""), versions: versions};
      });
    }).catch(function () {
      return findVersions(index + 1);
    });
  }

  function build(found) {
    var base = found.base;       /* relative path to the site root */
    var versions = found.versions;
    var path = window.location.pathname;

    var current = null;
    versions.forEach(function (version) {
      if (path.indexOf("/" + version + "/") !== -1) {
        current = version;
      }
    });

    var select = document.createElement("select");
    versions.forEach(function (version) {
      var option = document.createElement("option");
      option.value = base + version + "/";
      option.textContent = version;
      if (version === current) {
        option.selected = true;
      }
      select.appendChild(option);
    });
    select.addEventListener("change", function () {
      window.location.href = select.value;
    });

    var box = document.createElement("div");
    box.className = "version-switcher";
    var label = document.createElement("span");
    label.textContent = "Version:";
    box.appendChild(label);
    box.appendChild(select);
    document.body.appendChild(box);
  }

  findVersions(0).then(build).catch(function () {
    /* no versions.json: single-version build, no switcher */
  });
})();
