########################################################################################################################
# WARNING:
# When making any changes to this script, note that only the custom_gui file is auto-parsed
# If you make any changes that affect the generated interface/provinceview.gui code,
# you MUST manually copy the results into the src/interface/provinceview.gui file
# under the "province_window" windowType definition
########################################################################################################################

import os, textwrap, string, math

categories = [
	{
		"name": "farmlands",
		"prods": [
			{
				"name": "Crops",
				"id": 1
			},
			{
				"name": "Fiber",
				"id": 11
			},
			{
				"name": "Cash Crop",
				"id": 19
			},
			{
				"name": "Spices",
				"id": 20
			},
			{
				"name": "Sericulture",
				"id": 42
			},
			{
				"name": "Dye",
				"id": 12
			},
			{
				"name": "Settled Pasture",
				"id": 7
			},
			{
				"name": "Nomad Pasture",
				"id": 8
			}
		]
	},
	{
		"name": "forestry",
		"prods": [
			{
				"name": "Timber",
				"id": 13
			},
			{
				"name": "Game/Furs",
				"id": 21
			}
		]
	},
	{
		"name": "mines",
		"prods": [
			{
				"name": "Sea Salt",
				"id": 9
			},
			{
				"name": "Rock Salt",
				"id": 10
			},
			{
				"name": "Coal",
				"id": 14
			},
			{
				"name": "Metal",
				"id": 15
			},
			{
				"name": "Rare Metals",
				"id": 16
			},
			{
				"name": "Gold",
				"id": 17
			},
			{
				"name": "Silver",
				"id": 18
			},
			{
				"name": "Marble",
				"id": 41
			}
		]
	},
	{
		"name": "fishery",
		"prods": [
			{
				"name": "Fishery",
				"id": 6
			}
		]
	},
	{
		"name": "industry",
		"prods": [
			{
				"name": "Cottage Industry",
				"id": 38
			},
			{
				"name": "Houseware",
				"id": 24
			},
			{
				"name": "Textile",
				"id": 25
			},
			{
				"name": "Armament",
				"id": 26
			},
			{
				"name": "Ship",
				"id": 27
			},
			{
				"name": "Processed Material",
				"id": 28
			},
			{
				"name": "Silk",
				"id": 33
			},
			{
				"name": "Chinaware",
				"id": 34
			},
			{
				"name": "Carpet",
				"id": 35
			},
			{
				"name": "Glass",
				"id": 36
			},
			{
				"name": "Luxury Cloth",
				"id": 39
			},
			{
				"name": "Steel",
				"id": 40
			}
		]
	},
	{
		"name": "knowledge",
		"prods": [
			{
				"name": "Religious Knowledge",
				"id": 29
			},
			{
				"name": "Higher Learning",
				"id": 30
			}
		]
	},
	{
		"name": "commerce",
		"prods": [
			{
				"name": "Urban Commerce",
				"id": 32
			}
		]
	}
]

def getTextbox ( name, subname ):
	return textwrap.dedent( f'''\
		custom_text_box = {{
			name = {name}_{subname}
			tooltip = {name}_{subname}_tt
			potential = {{}}
		}}
		''')

def getSlotDefinitions( category_name, frame_number, prod, slot, prevs ):
	name = f'provinceview_tab3_{category_name}{len(prevs)}_{slot}'



	data = f'''\
		#### {prod[ 'name' ]} slot {slot}
		custom_window = {{
			name = {name}_window
			potential = {{
				Prod_HasProd = {{ Prod = {prod[ 'id' ]} }}
				calc_true_if = {{'''
	for prev in prevs:
		data += f'''
					Prod_HasProd = {{ Prod = {prev[ 'id' ]} }} # {prev[ 'name' ]}'''
	data += f'''
					amount = {slot}
				}}
				NOT = {{
					calc_true_if = {{'''
	for prev in prevs:
		data += f'''
						Prod_HasProd = {{ Prod = {prev[ 'id' ]} }} # {prev[ 'name' ]}'''
	data += f'''
						amount = {slot+1}
					}}
				}}
			}}
		}}
		custom_button = {{
			name = {name}
			tooltip = {name}_tt
			potential = {{}}
			trigger = {{}}
			effect = {{}}
			frame = {{ number = {frame_number} trigger = {{ owner = {{ has_country_flag = selected_tab3 }} }} }}
		}}
		'''

	data = textwrap.dedent( data )
	data += getTextbox( name, 'title' )
	for i in range( 1, 5 ):
		data += getTextbox( name, f'text_{i}' )
	return data

def readTemplate ( path ):
	with open( path, 'r' ) as f:
		return string.Template( f.read( ) )

def writeFile ( path, data ):
	os.makedirs( os.path.dirname( path ), exist_ok=True )
	with open( path, 'w' ) as f:
		f.write( data )

def write( dest ):
	filename = os.path.basename( __file__ )

	provinceViewTemplate = readTemplate( os.path.join( os.path.dirname( __file__ ), 'build_province_industry_gui', 'provinceview.gui.template' ) )

	customGuiData = ''
	provinceViewData = ''
	prevs = []
	for idx, category in enumerate( categories ):
		for prod in category[ 'prods' ]:
			for slot in range( 0, min( len( prevs )+1, 16 ) ):
				customGuiData += getSlotDefinitions( category[ 'name' ], idx+1, prod, slot, prevs )
				provinceViewData += provinceViewTemplate.safe_substitute({
					'category': category[ 'name' ],
					'idx': len( prevs ),
					'slot': slot,
					'xpos': 17 + ( 131 * ( slot % 4 ) ),
					'ypos': 523 + ( 51 * math.floor( slot / 4 ) )
				})
			customGuiData += '\n'
			prevs.append( prod )

	writeFile( os.path.join( dest, 'common', 'custom_gui', 'province_industry.txt' ), customGuiData )
	writeFile( os.path.join( dest, 'snippets', 'interface', 'provinceview.gui' ), provinceViewData )

if __name__ == '__main__':
	write( 'out' )
elif __name__ == '__build__':
	write( outdir )
