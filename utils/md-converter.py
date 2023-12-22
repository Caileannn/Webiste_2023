import re
import markdown2
import json
import os
import argparse

def read_md_file(md_file_path):
    with open(md_file_path, 'r', encoding="utf-8") as file:
        md_content = file.read()
    return md_content

def extract_content_by_type(md_content, content_type):
    pattern = f"^\s*# {content_type}\s*(.*?)\s*(?:\n|\Z)"
    matches = re.findall(pattern, md_content, re.DOTALL | re.MULTILINE)
    return matches

def convert_links(content):
    # Regular expression to match (text)[link]
    regex = r'\(([^)]*)\)\[([^\]]*)\]'

    # Replace each match with the corresponding anchor tag
    converted_text = re.sub(regex, r'<a href="\2" target="_blank">\1</a>', content)
    return converted_text

def add_text(content):
    converted_text = convert_links(content)
    html_text=f"""
        <span class="text-body">{converted_text}</span>
        """
    return html_text

def add_points(content):
    # Split content by \, returns an array
    points = content.split("\\")
    html_text = ""
    for point in points:
        html_text+=f"""
		<span class="list"><span class="point-symbol">&#8623;</span>{point}</span>
        """
    html_list=f"""
        <span class="list-point">{html_text}</span>
        """
    return html_list

def add_img_wide(content):
    html_text=f"""
        <div class="project-image"> <img class="text-body-image" src="{content}"> </div>
    """
    return html_text

def add_img_dbl(img1, img2):
    html_text=f"""
<div class="project-image-double">
			<img class="text-body-image-double" src="{img1}">
			<img class="text-body-image-double" src="{img2}">
		</div>
    """
    return html_text

def add_video(content):
    html_text=f"""
        <span class="text-body-video"><iframe title="vimeo-player" src="{content}" class="video-frame"   allowfullscreen></iframe></span>
    """
    return html_text

def add_showcase(year, title, place):
    html_text=f"""
        <span class="text-body"><span class="text-body-arrow">&#8623;</span><span class="text-body-date">({year})</span>{title},<span class="text-body-place">{place}</span></span>
    """
    return html_text

def add_index_item(title, year, section):
    html_text=f"""
<li onclick="openProjectFromIndex({section})">{title}, {year}</li>
    """
    return html_text

def generate_html_template(title, year, content, image, finger_position):
    r_hand = '👉'
    l_hand = '👈'
    l_pointer = 'sl-arrow'
    r_pointer = 'sr-arrow'

    if finger_position == 0:
        l_hand = '👉'
        l_pointer = 'sr-arrow'
    if finger_position == 2:
        r_hand = '👈'
        r_pointer = 'sl-arrow'

    html_template = f"""
    <section class="section"><div class="project-head-space" id="project-head-space"></div>
					<div class="project-window" id="project-window">
						<div class="arrow-slider">
							<div class="{l_pointer}" id="l_pointer">{l_hand}</div>
							<div class="s-emoji">༼;´༎ຶ ۝ ༎ຶ༽</div>
							<div class="{r_pointer}" id="r_pointer">{r_hand}</div>
						</div>
						<div class="project-text-header">
							<span>{title}, {year}.</span>
						</div>
						<div class="project-text-body" id="project-body-text">
							<div class="project-image">
								<img class="text-body-image" src="{image}">
							</div>
							{content}
						</div>
						
					</div>
					<div class="project-head-space"></div></section>
    """
    return html_template

def convert_md_to_html(md_content):
    html_content = markdown2.markdown(md_content)
    return html_content

def extract_content_sections(md_content):
    sections = re.split(r'\n\s*#\s*(\w+)(.*?)\s*(?=\n\s*#|$)', md_content, flags=re.DOTALL)[1:]
    content_list = []

    for i in range(0, len(sections), 3):
        section_type = sections[i].strip().lower()
        section_content = sections[i + 1].strip() if i + 1 < len(sections) else ''

        if section_type == 'text':
            content_list.append({'type': 'text', 'content': section_content})
        elif section_type == 'list':
            content_list.append({'type': 'list', 'content': section_content})
        elif section_type == 'imgw':
            content_list.append({'type': 'imgw', 'content': section_content})
        elif section_type == 'video':
            content_list.append({'type': 'video', 'content': section_content})
        elif section_type == 'showcase':
            year, title, place = map(str.strip, section_content.split('\\'))
            content_list.append({'type': 'showcase', 'year': year, 'title': title, 'place': place})
        elif section_type == 'imgdbl':
            img1, img2 = map(str.strip, section_content.split('\\'))
            content_list.append({'type': 'imgdbl', 'img1': img1, 'img2': img2})
        else:
            # Handle other section types as needed
            pass

    return content_list

def inject_html_into_file(html_file_path, generated_html, injection_marker):
    # Read the existing HTML file
    with open(html_file_path, 'r', encoding="utf-8") as file:
        original_html = file.read()

    # Find the position to inject the generated HTML
    injection_position = original_html.find(injection_marker)

    if injection_position != -1:
        # Split the original HTML into parts
        html_before_injection = original_html[:injection_position]
        html_after_injection = original_html[injection_position:]

        # Concatenate the parts with the generated HTML
        updated_html = f"{html_before_injection}\n{generated_html}\n{html_after_injection}"

        # Write the updated HTML back to the file
        with open(html_file_path, 'w', encoding="utf-8") as file:
            file.write(updated_html)
    else:
        print(f"Injection marker '{injection_marker}' not found in the HTML file.")

def remove_content_between_tags(html_file_path, flag):
    if (flag == 1):
        start_tag = "<!-- PROJECT START -->"
        end_tag = "<!-- PROJECT END -->"
        injection_point = "<!-- INJECTION POINT -->"
    if (flag == 2):
        start_tag = "<!-- INDEX START -->"
        end_tag = "<!-- INDEX END -->"
        injection_point = "<!-- INDEX INJECTION POINT -->"

    # Read the existing HTML file
    with open(html_file_path, 'r', encoding="utf-8") as file:
        original_html = file.read()

    #print(original_html)
    pattern = re.compile(fr"{re.escape(start_tag)}\s*(.*?)\s*{re.escape(end_tag)}", re.DOTALL)
    #return pattern.sub('', original_html)
    html_new = pattern.sub(f'{start_tag}\n{end_tag}', original_html)
    updated_html = pattern.sub(fr"{start_tag}\n{injection_point}\n{end_tag}", html_new)
    # Write the updated HTML back to the file
    with open(html_file_path, 'w', encoding="utf-8") as file:
        file.write(updated_html)

def update_href_links(content):
    regex = r'href="\.(.*?)"'
    # Use re.sub to replace matched paths with "..some_path"
    updated_text = re.sub(regex, r'href="..\1"', content)

    regex = r'src="\.(.*?)"'
    updated_text = re.sub(regex, r'src="..\1"', updated_text)

    return updated_text

def create_subpage(html, title):
    html_template=f"""
    <!DOCTYPE html>
<html>
	<head>
		<meta http-equiv="content-type" content="text/html; charset=utf-8" />
		<meta http-equiv="X-UA-Compatible" content="IE=edge">
		<title>cailean.finn | {title}</title>
        <link rel="icon" href="./icons/favicon.ico" type="image/x-icon">
		<link rel="android-chrome-icon" sizes="192x192" href="./icons/android-chrome-192x192.png">
		<link rel="android-chrome-icon" sizes="512x512" href="./icons/android-chrome-512x512.png">
		<link rel="apple-touch-icon" sizes="180x180" href="./icons/apple-touch-icon.png">
		<link rel="icon" type="image/png" sizes="32x32" href="./icons/favicon-32x32.png">
		<link rel="icon" type="image/png" sizes="16x16" href="./icons/favicon-16x16.png">
		<meta name="description" content="">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<link rel="preconnect" href="https://fonts.googleapis.com">
		<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
		<link href="https://fonts.googleapis.com/css2?family=Gothic+A1:wght@400;700&family=IBM+Plex+Mono:wght@100&display=swap" rel="stylesheet">
		<link href="https://fonts.googleapis.com/css2?family=Fira+Mono:wght@400;500;700&display=swap" rel="stylesheet">
		<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;1,100;1,200;1,300;1,400;1,500;1,600;1,700&family=IBM+Plex+Serif:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;1,100;1,200;1,300;1,400;1,500;1,600;1,700&display=swap" rel="stylesheet">
		<link rel="stylesheet" href="./css/sub.css">
	</head>
	<body>
		<div id="container">
			<a href="./"><div id="content-exit-container">&#8623;</div></a>
			<div id="project-cont" class="project-cont">
				<div class="flex-cont" id="slider-cont">
				<!-- PROJECT START -->
                {html}
    
<!-- INJECTION POINT -->
<!-- PROJECT END -->
				</div>
			</div>
		</div>
	</body>
</html>
    """
    # Create URL Name
    # Use title, but clear all whitespaces, and odd character's
    # Regular expression to match any character that is not a letter or a digit
    regex = r'[^a-zA-Z0-9]'
    html_updated = update_href_links(html_template)
    # Use re.sub to replace matched characters with an empty string
    cleaned_title = re.sub(regex, '', title)
    subpage_dir = '../public/works'
    # Create new HTML file, name it this, and write to it.
    new_file_path = f"{subpage_dir}/{cleaned_title}.html"
    with open(new_file_path, 'w', encoding='utf-8') as file:
        file.write(html_updated)
        print(f"created new html file: {cleaned_title}.html")





def main():
    # HTML body content (imgs, text, etc.)
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Process markdown files.')
    parser.add_argument('--draft', action='store_true', help='Include draft projects')
    args = parser.parse_args()

    content_body = f""
    md_dir = "../markdown"

    draft_flag = args.draft

    # Clear the existing nodes
    json_path = "../public/data.json"
    json_data = ''
    with open(json_path, 'r', encoding="utf-8") as json_file:
        json_data = json.load(json_file)
    json_data["nodes"] = []

    remove_content_between_tags('../public/index.html', 1)
    remove_content_between_tags('../public/index.html', 2)

    html_template = ''
    index_list_template = ''

    # Loop over each .md file
    files = os.listdir(md_dir)

    for idx, file in enumerate(files):
        # Check if it's a file (not a subdirectory)
        if os.path.isfile(os.path.join(md_dir, file)):
            # Process the file here
            content_body = f""
            print(f"Processing file: {file}")
            md_file_path = md_dir + "/" + file
            md_content = read_md_file(md_file_path)
            # Extracting metadata from the YAML front matter
            metadata_lines = md_content.split('---')[1].strip().split('\n')
            metadata = {}
            for line in metadata_lines:
                key, value = map(str.strip, line.split(':'))
                metadata[key] = value

            title = metadata.get('title', '')
            year = metadata.get('year', '')
            cover_img = metadata.get('page_img_path', '')
            node_img = metadata.get('cover_img_path', '')
            section = metadata.get('section', '')
            subpage = metadata.get('subpage', '')
            draft = metadata.get('draft', '')

            if draft == "true" and draft_flag is False:
                print("draft")
            elif (draft == "true" and draft_flag is True) or draft == 'false':
                # Add project to index list
                index_list_template += add_index_item(title, year, section)

                new_node = [
                    {
                        "title": f"{title}, {year}",
                        "path": f"{node_img}",
                        "width": 200,
                        "height": 80,
                        "section": section,
                        "tag": {"AI", "VIDEO"},
                        "strength": 0.01,
                        "subpage": f"{subpage}"
                    }
                ]

                # Convert sets to lists in new_nodes
                for node in new_node:
                    node["tag"] = list(node["tag"])

                json_data["nodes"].extend(new_node)

                # Extracting all content sections in order
                content_list = extract_content_sections(md_content)

                for attr in content_list:
                    if (attr.get('type') == 'text'):
                        content_body += add_text(attr.get('content'))
                    if (attr.get('type') == 'list'):
                        content_body += add_points(attr.get('content'))
                    if (attr.get('type') == 'imgw'):
                        content_body += add_img_wide(attr.get('content'))
                    if (attr.get('type') == 'video'):
                        content_body += add_video(attr.get('content'))
                    if (attr.get('type') == 'showcase'):
                        content_body += add_showcase(attr.get('year'), attr.get('title'), attr.get('place'))
                    if (attr.get('type') == 'imgdbl'):
                        content_body += add_img_dbl(attr.get('img1'), attr.get('img2'))

                finger_position = 1

                if idx == 0:
                    finger_position = 0
                if idx == len(files) - 1:
                    finger_position = 2
                
                # Generating HTML template
                html_content = generate_html_template(title, year, content_body, cover_img, finger_position)
                html_template += html_content
                create_subpage(html_content, title)
                # Writing the HTML template to a file
                # with open(html_output_path, 'w') as html_file:
                #     html_file.write(html_template)

    inject_html_into_file('../public/index.html', html_template, "<!-- INJECTION POINT -->")
    inject_html_into_file('../public/index.html', index_list_template, "<!-- INDEX INJECTION POINT -->")

    with open(json_path, 'w', encoding="utf-8") as json_file:
        json.dump(json_data, json_file, indent=2)
    

if __name__ == "__main__":
    main()
