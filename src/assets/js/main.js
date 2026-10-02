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



    // ========================================================
    // PROTOTYPE 2 - SERMON MEDIA CARDS
    // ========================================================

    const sermonCards = Array.from(
        document.querySelectorAll("[data-sermon-card]")
    );


    /*
    * Reset one card to its initial thumbnail-only state.
    */
    function resetSermonCard(card) {

        const cardTrigger = card.querySelector(
            "[data-sermon-card-trigger]"
        );

        const options = card.querySelector(
            "[data-sermon-card-options]"
        );

        const audioTrigger = card.querySelector(
            "[data-sermon-audio-trigger]"
        );

        const audioArea = card.querySelector(
            "[data-sermon-audio]"
        );

        const audioPlayer = audioArea
            ? audioArea.querySelector("audio")
            : null;


        /*
        * Pause audio if this card was playing.
        */
        if (audioPlayer) {
            audioPlayer.pause();
        }


        /*
        * Hide audio player.
        */
        if (audioArea) {
            audioArea.hidden = true;
        }


        /*
        * Reset Listen button.
        */
        if (audioTrigger) {

            audioTrigger.setAttribute(
                "aria-expanded",
                "false"
            );

            audioTrigger.textContent =
                "Listen";
        }


        /*
        * Hide action panel.
        */
        if (options) {
            options.hidden = true;
        }


        /*
        * Reset thumbnail trigger.
        */
        if (cardTrigger) {

            cardTrigger.setAttribute(
                "aria-expanded",
                "false"
            );

        }


        /*
        * Restore default card state.
        */
        card.classList.remove(
            "is-open",
            "is-audio-open"
        );

    }


    /*
    * Return the currently open sermon card.
    *
    * Only one card can be open at a time.
    */
    function getOpenSermonCard() {

        return sermonCards.find(
            (card) =>
                card.classList.contains("is-open")
        ) || null;

    }


    /*
    * Initialise each sermon card.
    */
    sermonCards.forEach((card) => {

        const cardTrigger = card.querySelector(
            "[data-sermon-card-trigger]"
        );

        const options = card.querySelector(
            "[data-sermon-card-options]"
        );

        const audioTrigger = card.querySelector(
            "[data-sermon-audio-trigger]"
        );

        const audioArea = card.querySelector(
            "[data-sermon-audio]"
        );

        const audioPlayer = audioArea
            ? audioArea.querySelector("audio")
            : null;


        /*
        * Thumbnail/card click.
        *
        * - Closed card -> open.
        * - Open card -> close.
        * - Opening one card closes every other card.
        */
        if (cardTrigger && options) {

            cardTrigger.addEventListener(
                "click",
                () => {

                    const isOpen =
                        card.classList.contains(
                            "is-open"
                        );


                    /*
                    * Clicking the currently open
                    * thumbnail closes that card.
                    */
                    if (isOpen) {

                        resetSermonCard(card);

                        return;
                    }


                    /*
                    * Close every other card first.
                    *
                    * This also pauses audio on any
                    * previously active card.
                    */
                    sermonCards.forEach(
                        (otherCard) => {

                            if (otherCard !== card) {

                                resetSermonCard(
                                    otherCard
                                );

                            }

                        }
                    );


                    /*
                    * Open the selected card.
                    */
                    options.hidden = false;

                    cardTrigger.setAttribute(
                        "aria-expanded",
                        "true"
                    );

                    card.classList.add(
                        "is-open"
                    );

                }
            );

        }


        /*
        * Listen / Hide Audio.
        */
        if (
            audioTrigger &&
            audioArea &&
            audioPlayer
        ) {

            audioTrigger.addEventListener(
                "click",
                async () => {

                    const isAudioOpen =
                        card.classList.contains(
                            "is-audio-open"
                        );


                    /*
                    * Hide audio but keep the
                    * card options open.
                    */
                    if (isAudioOpen) {

                        audioPlayer.pause();

                        audioArea.hidden = true;

                        card.classList.remove(
                            "is-audio-open"
                        );

                        audioTrigger.setAttribute(
                            "aria-expanded",
                            "false"
                        );

                        audioTrigger.textContent =
                            "Listen";

                        return;
                    }


                    /*
                    * Show audio player.
                    */
                    audioArea.hidden = false;

                    card.classList.add(
                        "is-audio-open"
                    );

                    audioTrigger.setAttribute(
                        "aria-expanded",
                        "true"
                    );

                    audioTrigger.textContent =
                        "Hide Audio";


                    /*
                    * User explicitly selected Listen,
                    * so playback may start here.
                    */
                    try {

                        await audioPlayer.play();

                    } catch (error) {

                        /*
                        * Keep the player visible if
                        * automatic playback is blocked.
                        */
                        console.warn(
                            "Audio playback could not start automatically.",
                            error
                        );

                    }

                }
            );

        }

    });


    /*
    * --------------------------------------------------------
    * CLOSE ACTIVE CARD WHEN CLICKING OUTSIDE IT
    * --------------------------------------------------------
    *
    * Clicking anywhere inside the active sermon card does
    * nothing here.
    *
    * This means YouTube, Listen, Hide Audio, Download Audio
    * and the audio controls continue to work normally.
    */
    document.addEventListener(
        "click",
        (event) => {

            const openCard =
                getOpenSermonCard();


            /*
            * Nothing is currently open.
            */
            if (!openCard) {
                return;
            }


            /*
            * Click happened somewhere inside the
            * active card, so leave it alone.
            */
            if (openCard.contains(event.target)) {
                return;
            }


            /*
            * Click happened outside the active card.
            */
            resetSermonCard(openCard);

        }
    );


    /*
    * --------------------------------------------------------
    * CLOSE ACTIVE CARD WITH ESCAPE
    * --------------------------------------------------------
    */
    document.addEventListener(
        "keydown",
        (event) => {

            if (event.key !== "Escape") {
                return;
            }


            const openCard =
                getOpenSermonCard();


            if (!openCard) {
                return;
            }


            resetSermonCard(openCard);

        }
    );


    /*
    * --------------------------------------------------------
    * CLOSE ACTIVE CARD WHEN IT LEAVES THE VIEWPORT
    * --------------------------------------------------------
    *
    * Partial visibility does NOT close the card.
    *
    * The card resets only when none of it remains visible.
    * If audio is playing, resetSermonCard() pauses it.
    */
    if ("IntersectionObserver" in window) {

        const sermonVisibilityObserver =
            new IntersectionObserver(
                (entries) => {

                    entries.forEach((entry) => {

                        const card =
                            entry.target;


                        /*
                        * Ignore closed cards.
                        */
                        if (
                            !card.classList.contains(
                                "is-open"
                            )
                        ) {
                            return;
                        }


                        /*
                        * Keep the card open while any
                        * part of it remains visible.
                        */
                        if (entry.isIntersecting) {
                            return;
                        }


                        /*
                        * Card has completely left
                        * the viewport.
                        */
                        resetSermonCard(card);

                    });

                },
                {
                    threshold: 0
                }
            );


        sermonCards.forEach((card) => {

            sermonVisibilityObserver.observe(
                card
            );

        });

    }


}); // End DOMContentLoaded