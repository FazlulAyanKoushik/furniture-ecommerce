from io import BytesIO
from openpyxl import Workbook
from rest_framework.views import APIView
from rest_framework.response import Response
from accountio.models import Organization


class OrganizationListExcelView(APIView):
    def get(self, request):
        categories = request.query_params.get("categories", None)
        organizations = Organization.objects.get_status_fair().order_by("name")

        if categories is not None:
            organizations = organizations.filter(
                categories__contains=[{"value": categories}]
            )
        # Create a new workbook and get the active worksheet
        wb = Workbook()
        ws = wb.active

        # Define the column headers
        headers = [
            "Name",
            "Display Name",
            "Slug",
            "Email",
            "Country",
            "Phone",
            "Website URLs",
        ]

        # Write the headers to the first row
        ws.append(headers)

        # Write organization data to subsequent rows
        for organization in organizations:
            row = [
                organization.name,
                organization.display_name,
                organization.slug,
                organization.email,
                organization.country,
                organization.phone,
                organization.website_url,
            ]
            ws.append(row)

        # Set column widths for better readability (optional)
        for column in ws.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(cell.value)
                except:
                    pass
            adjusted_width = (max_length + 2) * 1.2
            ws.column_dimensions[column_letter].width = adjusted_width

        # Save the workbook content to a BytesIO buffer
        buffer = BytesIO()
        wb.save(buffer)
        buffer.seek(0)

        # Create the response and set the appropriate headers
        response = Response(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = "attachment; filename=organizations.xlsx"

        # Set the response content as the workbook content
        response.content = buffer.getvalue()

        return response
