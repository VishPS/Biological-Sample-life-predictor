import pandas as pd
from math import exp

# Load dataset of ideal conditions
df = pd.read_csv(r"M:\assignments\biological sample life predictor\Biological_Sample_Storage_Filtered.csv")

# Weights for relevant columns (adjusted for higher impact of temperature)
weights = {
    "Storage Temperature": 0.8,
    "Humidity (%)": 0.2
}

def get_user_inputs():
    sample_types = df["Biological Sample"].unique()
    print("Available Sample Types:")
    for st in sample_types:
        print(f" - {st}")

    while True:
        sample_type = input("\nEnter sample type (exactly as above): ").strip()
        if sample_type in sample_types:
            break
        else:
            print("❌ Invalid sample type! Please enter a valid sample type from the list.")

    print("\n📥 Enter real-time environmental data:")
    while True:
        try:
            temperature = float(input("Temperature (°C): "))
            humidity = float(input("Humidity (%): "))
            break
        except ValueError:
            print("❌ Invalid input! Please enter numeric values.")

    iot_conditions = {
        "Storage Temperature": temperature,
        "Humidity (%)": humidity
    }

    return sample_type, iot_conditions

def predict_shelf_life(sample_type, iot_conditions):
    sample = df[df["Biological Sample"] == sample_type].iloc[0]
    base_life = float(sample["Max Preservation Time (Years)"])  # Keep in years
    k = float(sample["k (year^-1)"])

    deviation_score = 0
    for col, weight in weights.items():
        ideal = float(sample[col])
        actual = iot_conditions[col]
        deviation = (actual - ideal) ** 2  # Square the deviation to penalize large differences
        deviation_score += weight * deviation

    remaining_life = base_life * exp(-k * deviation_score)
    return round(remaining_life, 2), k

if __name__ == "__main__":
    sample_type, iot_input = get_user_inputs()

    predicted_life, k_value = predict_shelf_life(sample_type, iot_input)
    print(f"\n📊 Predicted shelf life for '{sample_type}' under given conditions:")
    print(f"  ➤ Using k = {k_value} (year⁻¹)")
    print(f"  🧪 Remaining Life: {predicted_life} years")
