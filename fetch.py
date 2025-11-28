import requests
import json
import time


APP_LIST_URL = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"
REVIEWS_URL = "https://store.steampowered.com/appreviews/{appid}?json=1&language=japanese"


def get_app_list():
    return requests.get(APP_LIST_URL).json()["applist"]["apps"]


def get_review_info(appid):
    try:
        url = REVIEWS_URL.format(appid=appid)
        res = requests.get(url).json()
        if "query_summary" not in res:
            return None

        summary = res["query_summary"]
        total = summary["total_reviews"]

        if total < 200:
            return None

        rating = round(summary["total_positive"] / total * 100, 2)

        return {
            "appid": appid,
            "total_reviews": total,
            "positive": summary["total_positive"],
            "rating": rating,
        }
    except:
        return None


def main():
    apps = get_app_list()
    results = []

    for app in apps[:5000]:
        info = get_review_info(app["appid"])
        if info:
            results.append(info)
        time.sleep(0.5)

    results.sort(key=lambda x: x["rating"], reverse=True)
    results = results[:3000]

    with open("ranking.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
