import requests
import json
import time


APP_IDS = range(1, 800000)  # 1〜80万の範囲を総当り
REVIEWS_URL = "https://store.steampowered.com/appreviews/{appid}?json=1&language=japanese"
INFO_URL = "https://store.steampowered.com/api/appdetails?appids={appid}&l=japanese"


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


def get_store_info(appid):
    try:
        res = requests.get(INFO_URL.format(appid=appid)).json()
        data = res[str(appid)]
        if not data["success"]:
            return None

        info = data["data"]
        return {
            "name": info.get("name", "Unknown"),
            "image": info.get("header_image", None),
        }
    except:
        return None


def main():
    results = []
    checked = 0

    for appid in APP_IDS:
        checked += 1
        review = get_review_info(appid)
        if not review:
            continue

        store = get_store_info(appid)
        if not store:
            continue

        game = {**review, **store}
        results.append(game)

        print(f"{appid} OK ({len(results)} games)")

        if len(results) >= 2000:
            break

        time.sleep(0.3)  # 負荷軽減

    results.sort(key=lambda x: x["rating"], reverse=True)

    with open("ranking.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print("Done! Collected:", len(results))


if __name__ == "__main__":
    main()
