import subprocess; subprocess.run(["playwright", "install", "chromium"])
import pandas as pd
from scraper import scrape_apollo_contacts
from drive_upload import upload_to_drive
import traceback


# Companies to ignore (already enriched)
already_enriched_companies = {
    "+Viktilabs", "Abundance and Health", "AgeMate", "Agilpharma GmbH", "AlgaeCal Inc.", "Amazonia Group",
    "Apyforme", "ASPRIVA GmbH", "Babs Bone Broth", "Bärbel Drexel GmbH", "BEARS WITH BENEFITS®",
    "Beautywise", "Bhava - Suplementos Clean Label", "Biofungi GmbH", "Biotikon", "BODYME", "Botanicapharma",
    "Botanycl Ltd", "Bowmar Nutrition", "BPI Sports", "BRAINEFFECT", "BrainJuice®", "Brandl Nutrition",
    "BUBS Naturals", "Bulletproof 360", "Casida GmbH", "Cell'innov SA", "CLAV GmbH",
    "Co.Exist Nutrition / 22 Days Nutrition", "Cosmix", "Create Wellness", "Cymbiotika",
    "D-LAB NUTRICOSMETICS", "Dr. Grandel GmbH", "Earth Fed Muscle", "edubily® Biochemie & Lifestyle",
    "Euro Nutrador B.V", "fayn GmbH", "Fitspire - Health | Wellness", "Force Factor", "gall-pharma gmbh",
    "Gevity Rx", "GIGAS NUTRITION B.V.", "Good Goods Germany GmbH", "GoodOnya Organic Hydration", "Guud",
    "Heidelberger Chlorella GmbH", "Hilma", "Hivital", "Hunter & Gather", "Igennus Healthcare Nutrition",
    "InnoNature", "Jolly Mama", "Ka'Chava", "Kardish Health Food Centre", "Known Nutrition", "Kos",
    "Korrect Life", "Kräuterhaus Sanct Bernhard KG", "Kyberg Vital GmbH", "Laboratoire LESCUYER",
    "Landish - The Smarter Food Company", "Lemme", "LoveBiome", "LUNARY", "LVLUP Health", "MacuHealth",
    "MADENA GmbH & Co. KG", "Momentous", "Moon Juice", "Mountain Peak Nutritionals", "MOVE YOUR FIT",
    "mse Pharmazeutika GmbH", "MYLILY - ORGANIC FEMCARE", "Natural Force", "Naturefy", "Natroceutics",
    "Natures Pure Blend", "NUTRI & CO", "Novoma", "Novomins Nutrition", "NoordCode", "Norwegian Fish Oil AS",
    "Nutra Holdings", "Nutra Organics", "NutriBrain", "Nutrimuscle", "NUCHIDO TIME+", "Nuun Hydration",
    "Ocean Drop", "Ogaenics", "Olimp Laboratories sp. z o.o.", "Om Mushroom Superfood", "omega3zone GmbH",
    "OMNi-BiOTiC® by Institut AllergoSan", "Onatera", "Organic Collagen Australia", "Organika Health Products",
    "Orzaks Medicine", "Ossa Organic", "Oxford Healthspan", "Perfect Supplements, LLC", "Personal Fav Co.",
    "Plant People", "Power Gummies", "Primal Harvest", "Primal State Performance GmbH", "Promix Nutrition",
    "Raab Vitalfood", "riise", "SanaExpert GmbH", "sanotact GmbH", "Savvy Nutrición", "Selvs",
    "Serotalin GmbH", "Simply Supplements", "SinoPlaSan AG", "So Shape", "Sooo.me™", "Sproos",
    "Sprout Living", "Starlabs Nutrition", "Steel Supplements", "Supply10", "Supply6", "Supply7",
    "Supply8", "Supply9", "Symphony Natural Health", "Terra Origin", "The Beauty Chef", "The Collagen Co",
    "The Harvest Table", "Total Nutrition Technology", "TruBrain", "Two Islands",
    "Underground Bio Labs (Panda Supplements)", "Vegavero", "VIDA GLOW", "Vimergy", "Vita Health",
    "Vitabay CV", "VitaBright", "VitaeLab AS", "Vitals Voedingssupplementen", "VitaminFit", "Vitl",
    "Waterboy", "Wellversed", "Wild Society Nutrition", "YPSI GmbH", "Zec+ Nutrition",
    "Zein Pharma Pharmaceutical Industries", "ZENpharma", "Zenement"
}

if __name__ == "__main__":
    try:
        print("🚀 Starting Apollo scraping...")

        companies = [
            # Apollo company profile URLs of companies NOT in already_enriched_companies
            ("https://app.apollo.io/#/companies/63e3b0a03d71b200014ea1a5", "Some New Company A"),
            ("https://app.apollo.io/#/companies/60f1e91ed5d7b500017a1a95", "Some New Company B")
        ]

        all_contacts = []
        for company_url, company_name in companies:
            if company_name in already_enriched_companies:
                print(f"⏩ Skipping {company_name}, already enriched.")
                continue

            print(f"🔍 Scraping contacts for: {company_name}")
            contacts = scrape_apollo_contacts(company_url)
            all_contacts.extend(contacts)

        print("💾 Saving contacts to CSV...")
        df = pd.DataFrame(all_contacts)
        df.to_csv("scraped_contacts.csv", index=False)

        print("📤 Uploading to Google Drive...")
        upload_to_drive("scraped_contacts.csv")

        print("✅ Done. All contacts scraped and uploaded.")

    except Exception as e:
        print("❌ An error occurred during scraping!")
        traceback.print_exc()
