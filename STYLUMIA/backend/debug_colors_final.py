from ai_stylist.schemas import Color

print("="*60)
print("VALID COLORS IN YOUR ENUM:")
print("="*60)

all_colors = [c.value for c in Color]
all_colors.sort()

for color in all_colors:
    print(f'    "{color}",')

print(f"\nTotal: {len(all_colors)} colors")