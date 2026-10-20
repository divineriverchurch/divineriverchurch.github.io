"use strict";


document.addEventListener("DOMContentLoaded", () => {

    // ========================================================
    // MOBILE NAVIGATION
    // ========================================================

    const navToggle = document.querySelector(
        "[data-nav-toggle]"
    );

    const navigation = document.querySelector(
        "[data-navigation]"
    );


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

        navToggle.addEventListener(
            "click",
            () => {

                const isOpen =
                    navigation.dataset.open === "true";

                setNavigationState(
                    !isOpen
                );

            }
        );


        navigation
            .querySelectorAll("a")
            .forEach((link) => {

                link.addEventListener(
                    "click",
                    () => {

                        setNavigationState(
                            false
                        );

                    }
                );

            });


        document.addEventListener(
            "keydown",
            (event) => {

                if (
                    event.key === "Escape" &&
                    navigation.dataset.open === "true"
                ) {

                    setNavigationState(
                        false
                    );

                    navToggle.focus();

                }

            }
        );


        const desktopQuery = window.matchMedia(
            "(min-width: 1024px)"
        );


        desktopQuery.addEventListener(
            "change",
            (event) => {

                if (event.matches) {

                    setNavigationState(
                        false
                    );

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

        return (
            document.documentElement.dataset.theme === "dark"
                ? "dark"
                : "light"
        );

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


    function setTheme(
        theme,
        persist = true
    ) {

        if (
            theme !== "light" &&
            theme !== "dark"
        ) {
            return;
        }

        document.documentElement.dataset.theme =
            theme;


        if (persist) {

            try {

                localStorage.setItem(
                    "drc-theme",
                    theme
                );

            } catch (error) {

                // Theme still works for the current page.

            }

        }


        updateThemeControl();

    }


    if (themeToggle) {

        updateThemeControl();


        themeToggle.addEventListener(
            "click",
            () => {

                const currentTheme =
                    getTheme();

                setTheme(
                    currentTheme === "dark"
                        ? "light"
                        : "dark"
                );

            }
        );

    }


    const systemTheme = window.matchMedia(
        "(prefers-color-scheme: dark)"
    );


    systemTheme.addEventListener(
        "change",
        (event) => {

            let storedTheme = null;


            try {

                storedTheme =
                    localStorage.getItem(
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
    // GIVE PAGE - CENTENARY BANK FLIP CARD
    // ========================================================

    const giveFlipCards = Array.from(
        document.querySelectorAll(
            "[data-give-flip-card]"
        )
    );


    giveFlipCards.forEach((card) => {

        const frontFace = card.querySelector(
            "[data-give-card-front]"
        );

        const backFace = card.querySelector(
            "[data-give-card-back]"
        );

        const openButton = card.querySelector(
            "[data-give-flip-open]"
        );

        const routes = Array.from(
            card.querySelectorAll(
                "[data-give-route]"
            )
        );

        const routeButtons = Array.from(
            card.querySelectorAll(
                "[data-give-route-target]"
            )
        );

        const backToAccountButtons =
            Array.from(
                card.querySelectorAll(
                    "[data-give-back-account]"
                )
            );


        if (
            !frontFace ||
            !backFace ||
            !openButton ||
            !routes.length
        ) {
            return;
        }


        const firstRoute =
            routes[0];

        const firstRouteId =
            firstRoute.dataset.giveRoute;


        // ----------------------------------------------------
        // Face Accessibility State
        // ----------------------------------------------------

        function setFaceState(flipped) {

            frontFace.setAttribute(
                "aria-hidden",
                String(flipped)
            );

            backFace.setAttribute(
                "aria-hidden",
                String(!flipped)
            );


            if ("inert" in frontFace) {

                frontFace.inert =
                    flipped;

                backFace.inert =
                    !flipped;

            } else {

                if (flipped) {

                    frontFace.setAttribute(
                        "inert",
                        ""
                    );

                    backFace.removeAttribute(
                        "inert"
                    );

                } else {

                    backFace.setAttribute(
                        "inert",
                        ""
                    );

                    frontFace.removeAttribute(
                        "inert"
                    );

                }

            }

        }


        // ----------------------------------------------------
        // Show One Transfer Route
        // ----------------------------------------------------

        function showRoute(
            routeId,
            moveFocus = false
        ) {

            let activeRoute = null;


            routes.forEach((route) => {

                const isActive =
                    route.dataset.giveRoute ===
                    routeId;


                route.hidden =
                    !isActive;

                route.classList.toggle(
                    "is-active",
                    isActive
                );


                if (isActive) {

                    activeRoute =
                        route;


                    const scrollArea =
                        route.querySelector(
                            ".give-transfer-route__instructions-scroll"
                        );


                    if (scrollArea) {

                        scrollArea.scrollTop =
                            0;

                    }

                }

            });


            if (
                moveFocus &&
                activeRoute
            ) {

                activeRoute.focus();

            }

        }


        // ----------------------------------------------------
        // Reset Card Route
        // ----------------------------------------------------

        function resetGiveCardRoute() {

            showRoute(
                firstRouteId,
                false
            );

        }


        // ----------------------------------------------------
        // Open Transfer Options
        // ----------------------------------------------------

        function openTransferOptions() {

            resetGiveCardRoute();

            card.classList.add(
                "is-flipped"
            );

            setFaceState(
                true
            );


            window.requestAnimationFrame(
                () => {

                    firstRoute.focus();

                }
            );

        }


        // ----------------------------------------------------
        // Return to Account
        // ----------------------------------------------------

        function returnToAccount() {

            card.classList.remove(
                "is-flipped"
            );

            setFaceState(
                false
            );

            resetGiveCardRoute();


            window.requestAnimationFrame(
                () => {

                    openButton.focus();

                }
            );

        }


        // ----------------------------------------------------
        // Initial State
        // ----------------------------------------------------

        card.classList.remove(
            "is-flipped"
        );

        setFaceState(
            false
        );

        resetGiveCardRoute();


        // ----------------------------------------------------
        // View Transfer Options
        // ----------------------------------------------------

        openButton.addEventListener(
            "click",
            () => {

                openTransferOptions();

            }
        );


        // ----------------------------------------------------
        // Transfer Route Navigation
        // ----------------------------------------------------

        routeButtons.forEach(
            (button) => {

                button.addEventListener(
                    "click",
                    () => {

                        const targetRouteId =
                            button.dataset
                                .giveRouteTarget;


                        if (!targetRouteId) {
                            return;
                        }


                        const targetExists =
                            routes.some(
                                (route) =>
                                    route.dataset.giveRoute ===
                                    targetRouteId
                            );


                        if (!targetExists) {
                            return;
                        }


                        showRoute(
                            targetRouteId,
                            true
                        );

                    }
                );

            }
        );


        // ----------------------------------------------------
        // Back to Account
        // ----------------------------------------------------

        backToAccountButtons.forEach(
            (button) => {

                button.addEventListener(
                    "click",
                    () => {

                        returnToAccount();

                    }
                );

            }
        );


        // ----------------------------------------------------
        // Escape Key
        // ----------------------------------------------------

        document.addEventListener(
            "keydown",
            (event) => {

                if (
                    event.key !== "Escape" ||
                    !card.classList.contains(
                        "is-flipped"
                    )
                ) {
                    return;
                }


                returnToAccount();

            }
        );

    });



    // ========================================================
    // SERMONS GALLERY - MEDIA CARDS
    // ========================================================

    const sermonCards = Array.from(
        document.querySelectorAll(
            "[data-sermon-card]"
        )
    );


    // --------------------------------------------------------
    // Reset Sermon Card
    // --------------------------------------------------------

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

        const audioPlayer =
            audioArea
                ? audioArea.querySelector(
                    "audio"
                )
                : null;


        if (audioPlayer) {

            audioPlayer.pause();

        }


        if (audioArea) {

            audioArea.hidden =
                true;

        }


        if (audioTrigger) {

            audioTrigger.setAttribute(
                "aria-expanded",
                "false"
            );

            audioTrigger.textContent =
                "Listen";

        }


        if (options) {

            options.hidden =
                true;

        }


        if (cardTrigger) {

            cardTrigger.setAttribute(
                "aria-expanded",
                "false"
            );

        }


        card.classList.remove(
            "is-open",
            "is-audio-open"
        );

    }


    // --------------------------------------------------------
    // Find Open Sermon Card
    // --------------------------------------------------------

    function getOpenSermonCard() {

        return (
            sermonCards.find(
                (card) =>
                    card.classList.contains(
                        "is-open"
                    )
            ) || null
        );

    }


    // --------------------------------------------------------
    // Initialise Sermon Cards
    // --------------------------------------------------------

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

        const audioPlayer =
            audioArea
                ? audioArea.querySelector(
                    "audio"
                )
                : null;


        // ----------------------------------------------------
        // View Options
        // ----------------------------------------------------

        if (
            cardTrigger &&
            options
        ) {

            cardTrigger.addEventListener(
                "click",
                () => {

                    const isOpen =
                        card.classList.contains(
                            "is-open"
                        );


                    if (isOpen) {

                        resetSermonCard(
                            card
                        );

                        return;

                    }


                    /*
                     * Opening a sermon closes any other
                     * currently open sermon.
                     */
                    sermonCards.forEach(
                        (otherCard) => {

                            if (
                                otherCard !== card
                            ) {

                                resetSermonCard(
                                    otherCard
                                );

                            }

                        }
                    );


                    options.hidden =
                        false;

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


        // ----------------------------------------------------
        // Optional Future Audio
        // ----------------------------------------------------

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


                    if (isAudioOpen) {

                        audioPlayer.pause();

                        audioArea.hidden =
                            true;

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


                    audioArea.hidden =
                        false;

                    card.classList.add(
                        "is-audio-open"
                    );

                    audioTrigger.setAttribute(
                        "aria-expanded",
                        "true"
                    );

                    audioTrigger.textContent =
                        "Hide Audio";


                    try {

                        await audioPlayer.play();

                    } catch (error) {

                        console.warn(
                            "Audio playback could not start automatically.",
                            error
                        );

                    }

                }
            );

        }

    });



    // ========================================================
    // SERMON CARD - CLICK OUTSIDE
    // ========================================================

    document.addEventListener(
        "click",
        (event) => {

            const openCard =
                getOpenSermonCard();


            if (!openCard) {
                return;
            }


            /*
             * Clicking anywhere inside the currently open
             * sermon card should leave it open.
             */
            if (
                openCard.contains(
                    event.target
                )
            ) {
                return;
            }


            /*
             * Load More is deliberately excluded here.
             *
             * If a sermon card is open and the visitor
             * selects Load More, the open sermon should
             * remain open while the next sermons appear.
             */
            const loadMoreControl =
                event.target.closest(
                    "[data-sermons-load-more]"
                );


            if (loadMoreControl) {
                return;
            }


            resetSermonCard(
                openCard
            );

        }
    );



    // ========================================================
    // SERMON CARD - ESCAPE
    // ========================================================

    document.addEventListener(
        "keydown",
        (event) => {

            if (
                event.key !== "Escape"
            ) {
                return;
            }


            const openCard =
                getOpenSermonCard();


            if (!openCard) {
                return;
            }


            resetSermonCard(
                openCard
            );

        }
    );



    // ========================================================
    // SERMON CARD - VIEWPORT VISIBILITY
    // ========================================================

    if (
        "IntersectionObserver" in window
    ) {

        const sermonVisibilityObserver =
            new IntersectionObserver(
                (entries) => {

                    entries.forEach(
                        (entry) => {

                            const card =
                                entry.target;


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
                            if (
                                entry.isIntersecting
                            ) {
                                return;
                            }


                            /*
                             * Card has fully left the
                             * viewport.
                             */
                            resetSermonCard(
                                card
                            );

                        }
                    );

                },
                {
                    threshold: 0
                }
            );


        sermonCards.forEach(
            (card) => {

                sermonVisibilityObserver.observe(
                    card
                );

            }
        );

    }



    // ========================================================
    // SERMONS GALLERY - LOAD MORE
    // ========================================================

    const sermonsGallery =
        document.querySelector(
            "[data-sermons-gallery]"
        );


    if (sermonsGallery) {

        const galleryItems = Array.from(
            sermonsGallery.querySelectorAll(
                "[data-sermons-gallery-item]"
            )
        );

        const loadMoreButton =
            sermonsGallery.querySelector(
                "[data-sermons-load-more]"
            );


        /*
         * Read the page size defined in sermons.html.
         *
         * Current value:
         *
         * data-sermons-page-size="12"
         *
         * If it is missing or invalid, use 12.
         */
        const configuredPageSize =
            Number.parseInt(
                sermonsGallery.dataset
                    .sermonsPageSize,
                10
            );


        const pageSize =
            Number.isInteger(
                configuredPageSize
            ) &&
            configuredPageSize > 0
                ? configuredPageSize
                : 12;


        /*
         * Initial gallery:
         *
         * 12 sermons maximum.
         */
        let visibleCount =
            Math.min(
                pageSize,
                galleryItems.length
            );


        // ----------------------------------------------------
        // Apply Gallery Visibility
        // ----------------------------------------------------

        function updateSermonGalleryVisibility() {

            galleryItems.forEach(
                (item, index) => {

                    item.hidden =
                        index >= visibleCount;

                }
            );


            /*
             * Hide the Load More control once every
             * sermon has been revealed.
             */
            if (loadMoreButton) {

                const allVisible =
                    visibleCount >=
                    galleryItems.length;


                loadMoreButton.hidden =
                    allVisible;

                loadMoreButton.disabled =
                    allVisible;

            }

        }


        /*
         * Establish initial state:
         *
         * Sermons 1-12 visible.
         * Sermons 13+ hidden.
         */
        updateSermonGalleryVisibility();


        // ----------------------------------------------------
        // Load More
        // ----------------------------------------------------

        if (loadMoreButton) {

            loadMoreButton.addEventListener(
                "click",
                () => {

                    /*
                     * Reveal another group of 12.
                     *
                     * 56 sermons:
                     *
                     * Initial  1-12
                     * Click 1  13-24
                     * Click 2  25-36
                     * Click 3  37-48
                     * Click 4  49-56
                     *
                     * The button then disappears.
                     */
                    visibleCount =
                        Math.min(
                            visibleCount +
                            pageSize,
                            galleryItems.length
                        );


                    updateSermonGalleryVisibility();

                }
            );

        }

    }


}); // End DOMContentLoaded