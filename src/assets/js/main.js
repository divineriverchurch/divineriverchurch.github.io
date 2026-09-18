"use strict";


document.addEventListener("DOMContentLoaded", () => {

    // ========================================================
    // MOBILE NAVIGATION
    // ========================================================

    const navToggle = document.querySelector("[data-nav-toggle]");
    const navigation = document.querySelector("[data-navigation]");


    function setNavigationState(open) {

        if (!navToggle || !navigation) {
            return;
        }

        navigation.dataset.open = String(open);

        navToggle.setAttribute(
            "aria-expanded",
            String(open)
        );

        const label = navToggle.querySelector(
            ".visually-hidden"
        );

        if (label) {
            label.textContent = open
                ? "Close navigation"
                : "Open navigation";
        }
    }


    if (navToggle && navigation) {

        navToggle.addEventListener("click", () => {

            const isOpen =
                navigation.dataset.open === "true";

            setNavigationState(!isOpen);

        });


        navigation
            .querySelectorAll("a")
            .forEach((link) => {

                link.addEventListener("click", () => {
                    setNavigationState(false);
                });

            });


        document.addEventListener("keydown", (event) => {

            if (
                event.key === "Escape" &&
                navigation.dataset.open === "true"
            ) {

                setNavigationState(false);

                navToggle.focus();
            }

        });


        const desktopQuery = window.matchMedia(
            "(min-width: 1024px)"
        );

        desktopQuery.addEventListener(
            "change",
            (event) => {

                if (event.matches) {
                    setNavigationState(false);
                }

            }
        );
    }



    // ========================================================
    // THEME
    // ========================================================

    const themeToggle = document.querySelector(
        "[data-theme-toggle]"
    );

    const themeIcon = document.querySelector(
        "[data-theme-icon]"
    );


    function getTheme() {

        return document.documentElement.dataset.theme === "dark"
            ? "dark"
            : "light";
    }


    function updateThemeControl() {

        if (!themeToggle) {
            return;
        }

        const theme = getTheme();

        const nextTheme =
            theme === "dark"
                ? "light"
                : "dark";

        themeToggle.setAttribute(
            "aria-label",
            `Switch to ${nextTheme} mode`
        );

        themeToggle.setAttribute(
            "title",
            `Switch to ${nextTheme} mode`
        );


        if (themeIcon) {

            themeIcon.textContent =
                theme === "dark"
                    ? "☀"
                    : "☾";
        }
    }


    function setTheme(theme, persist = true) {

        if (
            theme !== "light" &&
            theme !== "dark"
        ) {
            return;
        }

        document.documentElement.dataset.theme = theme;

        if (persist) {

            try {
                localStorage.setItem(
                    "drc-theme",
                    theme
                );
            } catch (error) {
                // Theme still works for current page.
            }
        }

        updateThemeControl();
    }


    if (themeToggle) {

        updateThemeControl();

        themeToggle.addEventListener("click", () => {

            const currentTheme = getTheme();

            setTheme(
                currentTheme === "dark"
                    ? "light"
                    : "dark"
            );

        });
    }


    const systemTheme = window.matchMedia(
        "(prefers-color-scheme: dark)"
    );


    systemTheme.addEventListener(
        "change",
        (event) => {

            let storedTheme = null;

            try {
                storedTheme = localStorage.getItem(
                    "drc-theme"
                );
            } catch (error) {
                storedTheme = null;
            }


            if (!storedTheme) {

                setTheme(
                    event.matches
                        ? "dark"
                        : "light",
                    false
                );

            }

        }
    );

});