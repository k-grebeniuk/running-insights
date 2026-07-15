from playwright.sync_api import Page


def wait_for_results(page: Page) -> None:

    page.wait_for_function(
        """
        () => {

            const headers = [
                ...document.querySelectorAll("[role='columnheader']")
            ];

            const hasHeader = headers.some(
                header => header.innerText.includes("Фамилия")
            );

            const rows = document.querySelectorAll(
                "[role='row']"
            );

            return hasHeader && rows.length > 5;
        }
        """
    )