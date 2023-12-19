import re
import markdown2
import json
import os

def read_md_file(md_file_path):
    with open(md_file_path, 'r') as file:
        md_content = file.read()
    return md_content

def extract_content_by_type(md_content, content_type):
    pattern = f"^\s*# {content_type}\s*(.*?)\s*(?:\n|\Z)"
    matches = re.findall(pattern, md_content, re.DOTALL | re.MULTILINE)
    return matches

def add_text(content):
    html_text=f"""
        <span class="text-body">{content}</span>
        """
    return html_text

def add_img_wide(content):
    html_text=f"""
        <div class="project-image"> <img class="text-body-image" src="{content}"> </div>
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
        elif section_type == 'imgw':
            content_list.append({'type': 'imgw', 'content': section_content})
        elif section_type == 'video':
            content_list.append({'type': 'video', 'content': section_content})
        elif section_type == 'showcase':
            year, title, place = map(str.strip, section_content.split('\\'))
            content_list.append({'type': 'showcase', 'year': year, 'title': title, 'place': place})
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

def main():
    # HTML body content (imgs, text, etc.)
    content_body = f""
    md_dir = "../markdown"

    # Clear the existing nodes
    json_path = "../public/data.json"
    json_data = ''
    with open(json_path, 'r') as json_file:
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
                if (attr.get('type') == 'imgw'):
                    content_body += add_img_wide(attr.get('content'))
                if (attr.get('type') == 'video'):
                    content_body += add_video(attr.get('content'))
                if (attr.get('type') == 'showcase'):
                    content_body += add_showcase(attr.get('year'), attr.get('title'), attr.get('place'))

            finger_position = 1

            if idx == 0:
                finger_position = 0
            if idx == len(files) - 1:
                finger_position = 2
            
            # Generating HTML template
            html_template += generate_html_template(title, year, content_body, cover_img, finger_position)
            # Writing the HTML template to a file
            # with open(html_output_path, 'w') as html_file:
            #     html_file.write(html_template)

    inject_html_into_file('../public/index.html', html_template, "<!-- INJECTION POINT -->")
    inject_html_into_file('../public/index.html', index_list_template, "<!-- INDEX INJECTION POINT -->")

    with open(json_path, 'w') as json_file:
        json.dump(json_data, json_file, indent=2)
    

if __name__ == "__main__":
    main()